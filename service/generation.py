import asyncio
import zipfile
import json
import os
from datetime import datetime
tasks_storage = {}


class AiAgent:

    async def create_zip_from_results(task_id: str, results: dict) -> str:
        """Создание ZIP архива с результатами"""
        zip_path = f"results/{task_id}.zip"

        with zipfile.ZipFile(zip_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
            for folder_idx, folder in enumerate(results["folders"]):
                folder_name = folder["name"]

                # Добавляем изображения в папку
                for img_idx in range(3):
                    # В реальности здесь будут реальные изображения от нейросети
                    img_data = f"Fake image content for {folder_name} - image {img_idx + 1}"
                    img_filename = f"image_{img_idx + 1}.txt"  # В реальности .jpg/.png
                    full_img_path = f"{folder_name}/{img_filename}"

                    zipf.writestr(full_img_path, img_data)

                # Добавляем JSON файл с описанием
                json_content = json.dumps(folder["description"], indent=2)
                zipf.writestr(f"{folder_name}/description.json", json_content)

        return zip_path

    async def simulate_ai_processing(self, task_id: str, image_path: str):
        """Имитация работы нейросети"""
        try:
            # Обновляем статус
            tasks_storage[task_id]["status"] = "processing"
            tasks_storage[task_id]["progress"] = 0

            # Имитируем обработку с прогрессом
            for i in range(5):
                await asyncio.sleep(2)  # Имитация работы
                tasks_storage[task_id]["progress"] = (i + 1) * 20

            # Создаем mock-результаты
            results = {
                "folders": [
                    {
                        "name": "detected_objects",
                        "images": [b"fake_image_data_1"] * 3,
                        "description": {"objects": ["cat", "dog", "car"], "confidence": [0.95, 0.87, 0.92]}
                    },
                    {
                        "name": "segmentation",
                        "images": [b"fake_image_data_2"] * 3,
                        "description": {"masks": 3, "resolution": "1024x768"}
                    },
                    {
                        "name": "analysis",
                        "images": [b"fake_image_data_3"] * 3,
                        "description": {"timestamp": str(datetime.now()), "version": "1.0"}
                    }
                ]
            }

            # Создаем ZIP архив
            zip_path = await self.create_zip_from_results(task_id, results)

            # Обновляем статус задачи
            tasks_storage[task_id].update({
                "status": "completed",
                "zip_path": zip_path,
                "completed_at": datetime.now().isoformat(),
                "file_size": os.path.getsize(zip_path)
            })

            # Очищаем временные файлы
            if os.path.exists(image_path):
                os.remove(image_path)

        except Exception as e:
            tasks_storage[task_id].update({
                "status": "error",
                "error": str(e)
            })


