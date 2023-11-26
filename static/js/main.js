// считывание матрицы для обработки 
function get_matrix()
{
    var matrixSize = document.getElementById('range_size_of_matrix').value // размер матрицы

    var matrixData = [] // пустая матрица

    // Получаем значения из полей ввода и добавляем их в двумерный массив matrixData
    for (var i = 1; i <= matrixSize; i++) {
        var row = [] // пустой одномерный массив

        for (var j = 1; j <= matrixSize; j++) {
            var input = document.getElementsByName('matrixCell' + i + '_' + j)[0].value;
            row.push(Number(input)) // добавляем значения в одномерный массив
        }
        matrixData.push(row) // добавляем одномерный массив в матрицу
    }

    var dataToSend = {
        size: matrixSize,
        matrix: matrixData
    };

    // отправляем данные на сервер
    fetch('/set_data_to_session', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json' // заголовок для корректного распознавания даннных на сервере
        },
        body: JSON.stringify(dataToSend) // отправляем данные
    })
}

// формирование таблицы
// diag = false/true - диагональ заблокирована/разблокирована
function show_matrix(diag = false)
{
    var size = document.getElementById('range_size_of_matrix').value // размер матрицы
        document.getElementById('matrix_size_div').classList.add('hidden') // прячем блок ввода размера матрицы

    var matrixContainer = document.getElementById('matrix_input'); // блок для вставки матрицы

    // создаем таблицу для матрицы смежности
    var table = document.createElement('table');
    table.id = 'matrix-table'

    // заголовок таблицы
    var thead = document.createElement('thead');
    var headerRow = document.createElement('tr');
    var emptyHeaderCell = document.createElement('th');
    headerRow.appendChild(emptyHeaderCell); //пустая ячейка в верхнем левом углу

    // Заголовки столбцов (вершины)
    for (var i = 1; i <= size; i++) {
        var vertexHeaderCell = document.createElement('td');
        vertexHeaderCell.textContent = 'x' + i;
        headerRow.appendChild(vertexHeaderCell);
    }
    thead.appendChild(headerRow);
    table.appendChild(thead);

    // Тело таблицы
    var tbody = document.createElement('tbody');
    for (var i = 1; i <= size; i++) {
        var row = document.createElement('tr');
        var vertexCell = document.createElement('td');
        vertexCell.textContent = 'x' + i; // подписи вершин (строки)
        row.appendChild(vertexCell);

        // Ячейки матрицы для ввода данных (input)
        for (var j = 1; j <= size; j++) {
            var cell = document.createElement('td');
            var input = document.createElement('input');       
            input.type = 'text';
            input.name = 'matrixCell' + i + '_' + j;
            if (!diag && i == j) { // блокировка диагонали
                input.disabled = true;
                input.value = 0;
            } 
            cell.appendChild(input);
            row.appendChild(cell);
        }
        tbody.appendChild(row);
    }
    table.appendChild(tbody);
    matrixContainer.appendChild(table);

    // разрешения на ввод только чисел
    matrixContainer.addEventListener('input', function(event) {
        var target = event.target;
    
        if (target.tagName === 'INPUT') {
            var inputValue = target.value;
            if (!/^\d+$/.test(inputValue)) { // Разрешаем только цифры
                // Очищаем поле ввода от некорректных символов
                target.value = inputValue.replace(/\D/g, '');
            }
        }
    });

    // создание кнопки ввода
    var button = document.createElement('button');
    button.id = 'sendMatrixBtn';
    button.type = 'button';
    button.className = 'text-white bg-gradient-to-r from-green-400 via-green-500 to-green-600 hover:bg-gradient-to-br focus:ring-4 focus:outline-none focus:ring-green-300 dark:focus:ring-green-800 font-medium rounded-lg text-sm px-5 py-2.5 text-center me-2 mb-2';
    button.textContent = 'Enter';
    button.addEventListener('click', function() {
        get_matrix(); // добавление функции get_matrix()
        var currentPath = window.location.pathname; // получаем текущий путь
        var resPath = currentPath + '/result'; // добавляем "/result" к текущему пути
        window.location.href = resPath; // переход к результату по нажатию кнопки
    });

    matrixContainer.appendChild(button); // добавление кнопки на страницу
}

    // // добавление кнопки ввода
    // matrixContainer.innerHTML = matrixContainer.innerHTML + '<div><button id="sendMatrixBtn" onclick="get_matrix()" type="button" class="text-white bg-gradient-to-r from-green-400 via-green-500 to-green-600 hover:bg-gradient-to-br focus:ring-4 focus:outline-none focus:ring-green-300 dark:focus:ring-green-800 font-medium rounded-lg text-sm px-5 py-2.5 text-center me-2 mb-2">Enter</button></div>'
    
    // var button = document.getElementById('sendMatrixBtn');

    // // ДОБАВЛЕНИЕ ПЕРЕХОДА В СООТВЕТСТВИИ С АЛГОРИТМОМ
    // // Добавляем обработчик события click
    // button.addEventListener('click', function() {
    //     var currentPath = window.location.pathname; // получаем текущий путь
    //     var resPath = currentPath + '/result'; // добавляем "/result" к текущему пути
    //     window.location.href = resPath; // переход к реузультату по нажатию кнопки
    // });

    //блок кода для вывода матрицы на странице с результатом
    // if (afterInput) // если была введена матрица
    //     var size = 2
    // else {
    //     var size = document.getElementById('range_size_of_matrix').value // размер матрицы
    //     document.getElementById('matrix_size_div').classList.add('hidden') // прячем блок ввода размера матрицы
    // }


function change_Size(element)
{
    var size = element.value
    document.getElementById('label_size_of_matrix').textContent = `Select size of Matrix: ${size}`
}

function set_theme()
{
    if (localStorage.getItem('color-theme') === 'dark' || (!('color-theme' in localStorage) && window.matchMedia('(prefers-color-scheme: dark)').matches)) {
        console.log('light')
        document.getElementById('theme-toggle-light-icon').classList.remove('hidden');
    } else {
        document.getElementById('theme-toggle-dark-icon').classList.remove('hidden');
        console.log('dark')
    }
}

function change_theme()
{
    var themeToggleBtn = document.getElementById('theme-toggle');
    var themeToggleDarkIcon = document.getElementById('theme-toggle-dark-icon');
    var themeToggleLightIcon = document.getElementById('theme-toggle-light-icon');

    themeToggleDarkIcon.classList.toggle('hidden');
    themeToggleLightIcon.classList.toggle('hidden');

    if (localStorage.getItem('color-theme')) {
        if (localStorage.getItem('color-theme') === 'light') {
            document.documentElement.classList.add('dark');
            localStorage.setItem('color-theme', 'dark');
        } else {
            document.documentElement.classList.remove('dark');
            localStorage.setItem('color-theme', 'light');
        }

    // if NOT set via local storage previously
    } else {
        if (document.documentElement.classList.contains('dark')) {
            document.documentElement.classList.remove('dark');
            localStorage.setItem('color-theme', 'light');
        } else {
            document.documentElement.classList.add('dark');
            localStorage.setItem('color-theme', 'dark');
        }
    }
}