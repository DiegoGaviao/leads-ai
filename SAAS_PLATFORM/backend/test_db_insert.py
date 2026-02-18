
from database import get_supabase_client
import logging

def test_insert():
    s = get_supabase_client()
    data = {
        "email": "test@example.com",
        "instagram_handle": "test_insta",
        "mission": "Test Mission",
        "enemy": "Test Enemy",
        "dor_cliente": "Test Pain",
        "method_name": "Test Method"
    }
    try:
        # Tenta inserir na tabela leads_ai_brands
        res = s.table("leads_ai_brands").insert(data).execute()
        print("✅ Insert Success:", res.data)
    except Exception as e:
        print("❌ Insert Error:", e)

if __name__ == "__main__":
    test_insert()
