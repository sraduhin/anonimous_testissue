from fastapi import UploadFile

from utils.parser import BaseFileValidator


class FileService:
    def __init__(
        self,
        JSONvalidator: BaseFileValidator,
        XMLValidator: BaseFileValidator,
    ):
        self.JSONvalidator = JSONvalidator()
        self.XMLValidator = XMLValidator()

    async def read_file(self, file: UploadFile):
        filedata = await file.read()
        if file.content_type == "application/json":
            data = await self.JSONvalidator.parse_file(filedata)
        elif file.content_type == "text/xml":
            data = await self.XMLValidator.parse_file(filedata)
        else:
            raise TypeError("Неправильный тип данных")
        if not data:
            raise ValueError(
                f"Не удалось прочитать содержимое файла {file.filename}"
            )
        return data
