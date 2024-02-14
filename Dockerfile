# Используем базовый образ Python
FROM python:3

# Устанавливаем рабочую директорию внутри контейнера
WORKDIR /usr/src/app

# Установка зависимостей Flask и других библиотек
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Установка nvm
COPY install_nvm.sh .
RUN chmod 777 ./install_nvm.sh
RUN ./install_nvm.sh

# Установка библиотек
COPY package-lock.json .
COPY package.json .
COPY tailwind.config.js .

RUN npm install

RUN npm install flowbite

# Копируем все файлы проекта внутрь контейнера
COPY Algorithms ./Algorithms
COPY static ./static
COPY templates ./templates
COPY app.py .
COPY config.py .
COPY fill_db.py .
COPY start_server.sh .

# Компиляция CSS-tailwind
RUN npm run compile-css

# Изменение прав
RUN chmod 777 ./fill_db.py
RUN chmod 777 ./app.py
RUN chmod 777 ./start_server.sh

EXPOSE 5000

# Запуск приложения
CMD ["/bin/bash", "start_server.sh"]
