# Используем базовый образ Python
FROM python:3

# Устанавливаем рабочую директорию внутри контейнера
WORKDIR /usr/src/app

# Установка nvm
COPY install_nvm.sh .
RUN chmod 777 ./install_nvm.sh
RUN ./install_nvm.sh

# Установка зависимостей Flask и других библиотек
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Копируем все файлы проекта внутрь контейнера
COPY Algorithms ./Algorithms
COPY static ./static
COPY templates ./templates
COPY app.py .
COPY config.py .
COPY fill_db.py .
COPY package-lock.json .
COPY package.json .
COPY tailwind.config.js .

# Установка библиотек
RUN npm install &> log.txt

RUN npm intall flowbite &> log.txt

RUN npm run compile-css &> log.txt

# Изменение прав
RUN chmod 777 ./fill_db.py

# Запуск приложения
CMD ["python", "app.py"]
