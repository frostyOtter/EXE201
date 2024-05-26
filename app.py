import pathlib
from dotenv import load_dotenv
import os
from fastapi import FastAPI, Body, HTTPException
from starlette.middleware.cors import CORSMiddleware
from src.engine import SearchEngine
wd = pathlib.Path(__file__).parent.resolve()
load_dotenv(dotenv_path=os.path.join(wd,'.env'))

es_id = os.environ.get("ES_ID")
es_api = os.environ.get("ES_API")
index_name = os.environ.get("INDEX_NAME")

search_engine = SearchEngine(
    id_name= es_id,
    api_key= es_api,
    index_name= index_name
)



app = FastAPI()

origins = ["*"]
 
app.add_middleware(
     CORSMiddleware,
     allow_origins=origins,
     allow_credentials=True,
     allow_methods=["*"],
     allow_headers=["*"],
)

### Standard health checks
@app.get("/", tags=["Health Check"])
async def root():
    return "hello world!"

@app.get("/get")
async def get_config():
    return

@app.post("/search_one_feature", tags=['search'])
async def search_one_feature(user_input:str,):
    results = search_engine.search_one_feature(input_query= user_input, input_feature= "ingredients")
    if results != {}:
        return results['hits']['hits']
    return {}

# [{'_index': 'recipes',
#   '_id': 'T3tJs48BIJMJcnTjzG8I',
#   '_score': 0.2876821,
#   '_ignored': ['cook.keyword'],
#   '_source': {'title': 'trứng chiên hành thơm ngon, mềm xốp',
#    'ingredients': '3 quả trứng gà hoặc trứng vịt, 2 củ hành khô, hành lá, hạt nêm, nước mắm, bột ngọt, hạt tiêu, dầu ăn',
#    'time': 10,
#    'cook': 'Cách làm trứng chiên\nBước 1 Sơ chế nguyên liệu\nHành khô bóc vỏ, rửa sạch rồi thái lát mỏng.\nHành lá rửa sạch, thái nhỏ.\nĐập trứng ra tô, cho một ít hạt nêm, nước mắm, bột ngọt, hạt tiêu theo khẩu vị sau đó đánh tan. Tiếp đến cho hành lá và cho thêm 1 thìa dầu ăn vào khuấy đều để trứng sau khi chiên không bị khô.\nBước 2 Chiên trứng\nBắc chảo lên bếp, cho dầu ăn vào, cho hành khô vào phi thơm, sau đó cho trứng vào chiên.\nĐun nhỏ lửa chiên đến khi trứng vàng xốp thì khéo léo cuộn trứng lại cho đẹp mắt rồi tắt bếp.\nGắp trứng ra dĩa và dùng dao cắt miếng vừa ăn.\nBước 3 Thành phẩm\nTrứng chiên là món ăn vừa dễ làm vừa thơm ngon. Món ăn hấp dẫn ăn cùng với cơm nóng thì còn gì bằng. Chân chờ gì nữa mà không vào bếp trổ tài cho cả nhà nào!\n',
#    'images': 'link/to/images.jpg'}}]

@app.post("/search_multi_features", tags=['search'])
async def search_multi_features(user_input:str,):
    results = search_engine.search_many_feature(input_query = user_input, input_features= ["title", "ingredients"])
    if results != {}:
        return results['hits']['hits']
    return {}

# [{'_index': 'recipes',
#   '_id': 'T3tJs48BIJMJcnTjzG8I',
#   '_score': 0.2876821,
#   '_ignored': ['cook.keyword'],
#   '_source': {'title': 'trứng chiên hành thơm ngon, mềm xốp',
#    'ingredients': '3 quả trứng gà hoặc trứng vịt, 2 củ hành khô, hành lá, hạt nêm, nước mắm, bột ngọt, hạt tiêu, dầu ăn',
#    'time': 10,
#    'cook': 'Cách làm trứng chiên\nBước 1 Sơ chế nguyên liệu\nHành khô bóc vỏ, rửa sạch rồi thái lát mỏng.\nHành lá rửa sạch, thái nhỏ.\nĐập trứng ra tô, cho một ít hạt nêm, nước mắm, bột ngọt, hạt tiêu theo khẩu vị sau đó đánh tan. Tiếp đến cho hành lá và cho thêm 1 thìa dầu ăn vào khuấy đều để trứng sau khi chiên không bị khô.\nBước 2 Chiên trứng\nBắc chảo lên bếp, cho dầu ăn vào, cho hành khô vào phi thơm, sau đó cho trứng vào chiên.\nĐun nhỏ lửa chiên đến khi trứng vàng xốp thì khéo léo cuộn trứng lại cho đẹp mắt rồi tắt bếp.\nGắp trứng ra dĩa và dùng dao cắt miếng vừa ăn.\nBước 3 Thành phẩm\nTrứng chiên là món ăn vừa dễ làm vừa thơm ngon. Món ăn hấp dẫn ăn cùng với cơm nóng thì còn gì bằng. Chân chờ gì nữa mà không vào bếp trổ tài cho cả nhà nào!\n',
#    'images': 'link/to/images.jpg'}}]