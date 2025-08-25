PROMPTS = {
    "ampere_check": '''
        Is the Amperes value greater than 0. Hãy đưa ra kết quả theo 4 bước :
        Bước 1: Summary question
        Bước 2: Caption: Review các đối tượng trong ảnh liên quan đến câu hỏi
        Bước 3: Reasoning dựa trên Summary, Caption
        Bước 4: Answer OK or NOK!
        Trả lời output dưới dạng JSON, không thêm chữ khác. 
        {
          "summary": "...",
          "caption": "...",
          "reasoning": "...",
          "answer": "OK" hoặc "NOK"
        }
    ''', 
    "dan_lanh_co_xo_nuoc": '''
        Có túi bạt đang bọc che dàn lạnh không, có xô nước sạch không? Hãy đưa ra kết quả theo 4 bước :
        Bước 1: Summary question
        Bước 2: Caption: Review các đối tượng trong ảnh liên quan đến câu hỏi
        Bước 3: Reasoning dựa trên Summary, Caption
        Bước 4: Answer OK or NOK!
        Trả lời output dưới dạng JSON, không thêm chữ khác. 
        {
          "summary": "...",
          "caption": "...",
          "reasoning": "...",
          "answer": "OK" nếu có túi bạt đang bọc dàn lạnh và có xô nước sạch, nếu không thì "NOK"
        }
    ''',
}

LINKS = {
    'ampere_check': "sample_images//ampe_kim_dong_ho_do_gas", 
    'dan_lanh_co_xo_nuoc': "sample_images//bao_duong_dan_lanh\dan_lanh_co_xo_nuoc_co_bat", 
}

