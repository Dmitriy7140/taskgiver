# from yandex_cloud_ml_sdk import YCloudML
# from config import YAPI_KEY, FOLDER_ID, MODEL_URL
#
# sdk = YCloudML(folder_id=FOLDER_ID, auth=YAPI_KEY)
# model = sdk.models.completions(MODEL_URL)
#
# def generate_review(prompt: str) -> str:
#     result = model.run(
#         prompt,
#
#
#     )
#     print(result)
#     return result.alternatives[0].text
