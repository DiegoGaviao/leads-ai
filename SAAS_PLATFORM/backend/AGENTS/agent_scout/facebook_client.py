import requests
import logging
from typing import Dict, List, Optional
import os
import json
from dotenv import load_dotenv

load_dotenv()

class FacebookClient:
    """
    Cliente para interagir com a Graph API da Meta (Instagram).
    Portado da lógica original do dashboard.php.
    """
    def __init__(self):
        self.app_id = os.getenv("META_APP_ID", "880409131510410")
        self.app_secret = os.getenv("META_APP_SECRET", "a0e3921d5e79cbbc81420cc9a14b28bc")
        self.api_version = "v18.0"
        self.base_url = f"https://graph.facebook.com/{self.api_version}"

    def get_instagram_accounts(self, access_token: str) -> List[Dict]:
        """
        Busca as contas do Instagram Business vinculadas ao usuário.
        """
        endpoint = f"{self.base_url}/me/accounts"
        params = {
            "fields": "name,picture,instagram_business_account{id,username,profile_picture_url}",
            "access_token": access_token
        }
        
        try:
            response = requests.get(endpoint, params=params)
            response.raise_for_status()
            data = response.json()
            
            accounts = []
            for page in data.get("data", []):
                ig_data = page.get("instagram_business_account")
                if ig_data:
                    accounts.append({
                        "name": page.get("name"),
                        "ig_id": ig_data.get("id"),
                        "username": ig_data.get("username"),
                        "pic": ig_data.get("profile_picture_url")
                    })
            return accounts
            
        except requests.exceptions.RequestException as e:
            logging.error(f"❌ Erro ao buscar contas IG: {e}")
            return []

    def exchange_code_for_access_token(self, code: str, redirect_uri: str) -> str:
        """
        Troca o `code` do OAuth do Facebook por um `access_token`.

        Observação (MVP): o frontend inicia o OAuth e retorna o `code` via redirect.
        Essa troca acontece aqui no backend usando APP_SECRET.
        """
        endpoint = f"{self.base_url}/oauth/access_token"
        params = {
            "client_id": self.app_id,
            "redirect_uri": redirect_uri,
            "client_secret": self.app_secret,
            "code": code,
        }

        response = requests.get(endpoint, params=params, timeout=30)
        response.raise_for_status()
        data = response.json() or {}

        token = data.get("access_token")
        if not token:
            raise ValueError(f"Resposta inesperada do OAuth (sem access_token): {data}")

        return token

    def get_posts_data(self, ig_account_id: str, access_token: str, limit: int = 50) -> List[Dict]:
        """
        Busca métricas detalhadas dos posts (Reels, Carrossel, Imagem).
        Tenta replicar a lógica de batch do PHP ou fazer sequencial otimizado.
        """
        endpoint = f"{self.base_url}/{ig_account_id}/media"
        
        # Campos solicitados (igual ao dashboard.php)
        fields = [
            "id", "caption", "media_type", "media_product_type", 
            "permalink", "thumbnail_url", "timestamp", 
            "comments_count", "like_count", "shortcode"
        ]
        # Tentativa de pegar play_count direto (pode falhar em algumas versões, mas o PHP usava)
        fields.append("play_count") 
        
        params = {
            "fields": ",".join(fields),
            "limit": limit,
            "access_token": access_token
        }

        try:
            response = requests.get(endpoint, params=params)
            response.raise_for_status()
            media_items = response.json().get("data", [])
            
            posts_data = []
            
            # Para cada post, precisamos buscar os insights detalhados
            # O PHP usava Batch Request para ser rápido. Vamos implementar Batch aqui também.
            
            batch_payload = []
            for media in media_items:
                # Definir métricas baseadas no tipo (Logic portado do PHP)
                metrics = "reach,saved" # Básico
                
                m_type = media.get("media_type")
                p_type = media.get("media_product_type")
                
                if m_type == "VIDEO" or p_type == "REELS":
                    metrics += ",shares" # Video/Reels
                elif m_type == "CAROUSEL_ALBUM":
                    metrics += ",profile_visits" # Carrossel
                else:
                    metrics += ",shares,profile_visits" # Imagem
                
                batch_payload.append({
                    "method": "GET",
                    "relative_url": f"{media['id']}/insights?metric={metrics}"
                })

            if not batch_payload:
                return []

            # Enviar Batch Request (POST na raiz graph)
            # Graph API espera o parâmetro `batch` no body (form-encoded).
            # Usar JSON aqui pode quebrar silenciosamente em alguns cenários.
            batch_response = requests.post(
                f"https://graph.facebook.com/{self.api_version}/",
                params={"access_token": access_token},
                data={"batch": json.dumps(batch_payload)},
                timeout=30
            )
            batch_response.raise_for_status()
            batch_results = batch_response.json()
            
            # Processar Resultados
            for i, result in enumerate(batch_results):
                media = media_items[i]
                code = result.get("code")
                body = json.loads(result.get("body", "{}"))
                
                stats = {
                    "reach": 0, "saved": 0, "shares": 0, "profile_visits": 0, 
                    "plays": media.get("play_count", 0)
                }
                
                if code == 200 and "data" in body:
                    for metric in body["data"]:
                        if "values" in metric and len(metric["values"]) > 0:
                            stats[metric["name"]] = metric["values"][0]["value"]
                
                # Consolidar objeto final
                # Fallback de Views (se plays for 0, usa reach)
                final_views = stats["plays"] if stats["plays"] > 0 else stats["reach"]
                
                # Interações Totais (Likes + Coments + Saves)
                total_interactions = (media.get("like_count", 0) + 
                                    media.get("comments_count", 0) + 
                                    stats["saved"])

                posts_data.append({
                    "external_id": media.get("id"),
                    "tema": media.get("caption", "")[:50] + "...", # Resumo da legenda
                    "full_caption": media.get("caption", ""),
                    "type": media.get("media_product_type") or media.get("media_type"),
                    "date": media.get("timestamp"),
                    "link": media.get("permalink"),
                    "views": final_views,
                    "likes": media.get("like_count", 0),
                    "comments": media.get("comments_count", 0),
                    "saves": stats["saved"],
                    "shares": stats["shares"],
                    "reach": stats["reach"],
                    "interactions": total_interactions
                })
                
            return posts_data

        except Exception as e:
            logging.error(f"❌ Erro ao buscar posts: {e}")
            return []
