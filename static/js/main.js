// просьба сильно не редачить эту красоту :)

// функция смены шаблона страницы ввода алгоритма
var route = {
    dm: '/topological_sort/demukron',
    dfs: '/topological_sort/depth_first_search',
    ml: '/strong_connectivity/malgrange',
    ks: '/strong_connectivity/kosaraju',
    pr: '/minimal_spanning_tree/prim',
    kr: '/minimal_spanning_tree/kraskal',
    ds: '/shortest_path/dijkstra',
    bf: '/shortest_path/bellman–ford',
    fl: '/shortest_path/floyd_warshall',
};


function setDbdata(id)
{
    dataToSend = {
        alg_code: id
    };
    
    // отправляем информацию на сервер
    fetch('/set_dbdata', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json' // заголовок для корректного распознавания даннных на сервере
        },
        body: JSON.stringify(dataToSend) // отправляем данные
    })
    .then(response => {
        if (!response.ok) {
            throw new Error('Произошла ошибка при получении данных');
        }
        return response.json();
    })
    .then(data => {
        // Действия с полученными данными data
        console.log('Данные успешно получены:', data);
        // Перенаправление на другую страницу
        window.location.href = route[id];
    })
    .catch(error => {
        console.error('Произошла ошибка:', error);
    });
}

function changeTemplate(id, id_desc, text)
{
    var title = document.querySelector('.algorithmTitle'); // получени элемента по имени класса
    if (title) {
        title.textContent = text; // смена заголовка
        title.id = id;
    }

    var link = document.getElementById('getResult');
    if (link) {
        link.href = route[id]
    }

    // Получить все элементы <p> внутри <div> с классом algorithmDesc
    var desc = document.querySelectorAll('.algorithmDesc');

    // Перебрать полученные элементы и скрыть их
    if (desc.length > 0) {
        // Перебрать полученные элементы и добавить класс 'hidden', чтобы скрыть их
        desc.forEach(function(element) {+
            element.classList.add('hidden'); // Добавить класс 'hidden' для скрытия элементов <p>
        });
    } else {
        console.log('Элементы не найдены'); // Вывести сообщение об отсутствии элементов
    }
    document.getElementById(id_desc).classList.remove('hidden')
}

// считывание матрицы для обработки
function get_matrix()
{
    // отключение ввода
    var inputs = document.querySelectorAll('#matrix-table input[type="text"], #matrix-table input[type="checkbox"]');
    inputs.forEach(function(input) {
        input.disabled = true; // отключить возможность ввода
    });

    // отключение ввода пути
    var inputs = document.querySelectorAll('#path input[type="text"]');
    if (inputs) {
        inputs.forEach(function(input) {
            input.disabled = true; // отключить возможность ввода
        });
    }

    var matrixSize = document.getElementById('range_size_of_matrix').value // размер матрицы

    var matrixData = [] // пустая матрица

    // Получаем значения из полей ввода и добавляем их в двумерный массив matrixData
    for (var i = 1; i <= matrixSize; i++) {
        var row = [] // пустой одномерный массив

        for (var j = 1; j <= matrixSize; j++) {
            var input = document.getElementsByName('matrixCell' + i + '_' + j)[0];
            var type = input.type
            if (type == 'text')
                row.push(Number(input.value)) // добавляем значения в одномерный массив
            else if (type == 'checkbox') 
                row.push(Number(input.checked))              
        }
        matrixData.push(row) // добавляем одномерный массив в матрицу
    }

    // получение пути
    var pathFlag = false
    var start = document.getElementById('from')
    var finish = document.getElementById('to')
    if (start && finish) 
        start = Number(start.value)
        finish = Number(finish.value)
        pathFlag = true
        
    if (pathFlag) {
          var dataToSend = {
            size: matrixSize,
            matrix: matrixData,
            pathFlag: pathFlag,
            start_ver: start,
            finish_ver: finish
        };
    }
    else {
        var dataToSend = {
            size: matrixSize,
            matrix: matrixData,
            pathFlag: pathFlag
        };
    }
        
    // отправляем данные на сервер
    fetch('/set_data_to_session', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json' // заголовок для корректного распознавания даннных на сервере
        },
        body: JSON.stringify(dataToSend) // отправляем данные
    })

    document.getElementById('send-btnContainer').classList.add('hidden') // прячем кнопки ввода матрицы

    var buttonContainer = document.getElementById('change-btnContainer');
    buttonContainer.classList.remove('hidden')

}

// изменение матрицы
function edit_matrix(clear = true)
{
    var inputs = document.querySelectorAll('#matrix-table input[type="text"], #matrix-table input[type="checkbox"]');
    if (clear) {
        inputs.forEach(function(input) {
            input.value = ''; // очистить содержимое input
            input.checked = false; // снять галочку, если это checkbox
        });   
    } else {
        inputs.forEach(function(input) {
            if (!input.classList.contains('blocked'))
                input.disabled = false; // включить возможность ввода
        });
            // включение вомзожности ввода пути
            var inputs = document.querySelectorAll('#path input[type="text"]');
            if (inputs) {
                inputs.forEach(function(input) {
                    if (!input.classList.contains('blocked'))
                        input.disabled = false; // отключить возможность ввода
                });
            }

        document.getElementById('send-btnContainer').classList.remove('hidden') // возвращаем кнопки ввода матрицы
        document.getElementById('change-btnContainer').classList.add('hidden') // прячем кнопки получения результата
    }
}

function back_to_size() 
{
    document.getElementById('changeMatrixSizeLink').classList.add('hidden')
    document.getElementById('matrix_input').classList.add('hidden')
    document.getElementById('matrix_size_div').classList.remove('hidden')
}

// формирование таблицы
// diag = false/true - разблокирована/диагональ заблокирована
// bin = false/true - обычная с весами/бинарная
// direction = false/true - нет/есть поле для ввода нач. и конечной вершин
function show_matrix(blockDiag = false, bin = false, direction = false)
{
    sizeButton = document.getElementById('changeMatrixSizeLink')
    sizeButton.classList.remove('hidden')
    sizeButton.addEventListener('click', function() {
        back_to_size(); // добавление функции get_matrix()
    });

    var size = document.getElementById('range_size_of_matrix').value // размер матрицы
    document.getElementById('matrix_size_div').classList.add('hidden') // прячем блок ввода размера матрицы

    var matrixContainer = document.getElementById('matrix_input'); // блок для вставки матрицы
    matrixContainer.innerHTML = ''
    matrixContainer.classList.remove('hidden')
    matrixContainer.classList.add('flex', 'flex-col', 'justify-center', 'items-center', 'mb-5');
    matrixContainer.style.width = '100px';


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
        index = i - 1;
        vertexHeaderCell.textContent = 'x' + index;
        vertexHeaderCell.classList.add('dark:text-gray-400')
        headerRow.appendChild(vertexHeaderCell);
    }
    thead.appendChild(headerRow);
    table.appendChild(thead);

    // Тело таблицы
    var tbody = document.createElement('tbody');
    for (var i = 1; i <= size; i++) {
        var row = document.createElement('tr');
        var vertexCell = document.createElement('td');
        index = i - 1;
        vertexCell.textContent = 'x' + index; // подписи вершин (строки)
        vertexCell.classList.add('dark:text-gray-400')
        row.appendChild(vertexCell);

        // Ячейки матрицы для ввода данных (input)
        for (var j = 1; j <= size; j++) {
            var cell = document.createElement('td');
            var input = document.createElement('input');
            if (!bin)
                input.type = 'text';
            else
                input.type = 'checkbox';
            input.name = 'matrixCell' + i + '_' + j;
            input.classList.add('dark:bg-gray-800')
            if (blockDiag && i == j) { // блокировка диагонали
                input.disabled = true;
                input.value = 0;
                input.className = "blocked"
                input.classList.add('bg-gray-500')
            } 
            cell.appendChild(input);
            row.appendChild(cell);
        }
        tbody.appendChild(row);
    }
    table.appendChild(tbody);
    matrixContainer.appendChild(table);

    if (direction) {
        // добавление пути
        // создаем блок для элементов "Из" и "В"
        var ioContainer = document.createElement('div');
        ioContainer.className = 'flex items-center justify-between p-4';
        ioContainer.id = 'path'

        // создаем элементы label для подписей "Из" и "В"
        var fromLabel = document.createElement('label');
        fromLabel.textContent = 'Из:';
        fromLabel.className = 'p-1 dark:text-gray-400';
    
        var toLabel = document.createElement('label');
        toLabel.textContent = 'В:';
        toLabel.className = 'p-1 dark:text-gray-400';

        // добавляем элементы label в блок "Из/В"
        ioContainer.appendChild(fromLabel);

        // Создаем элементы input для "Из" и "В"
        var fromInput = document.createElement('input');
        fromInput.type = 'text';
        fromInput.classList.add('border', 'rounded', 'dark:bg-gray-800');
        fromInput.id = 'from'

        var toInput = document.createElement('input');
        toInput.type = 'text';
        toInput.classList.add('border', 'rounded', 'dark:bg-gray-800');
        toInput.id = 'to'

        // Добавляем элементы input в блок "Из/В"
        ioContainer.appendChild(fromInput);

        // Добавляем подпись "В" после input "Из"
        ioContainer.appendChild(toLabel);

        // Добавляем элемент input "В" после подписи "В"
        ioContainer.appendChild(toInput);

        // Добавляем блок "Из/В" под таблицей с матрицей
        matrixContainer.appendChild(ioContainer);
    }
    
    // разрешения на ввод только чисел
    matrixContainer.addEventListener('input', function(event) {
        var target = event.target;
    
        if (target.tagName === 'INPUT') {
            var inputValue = target.value;
            // Разрешаем только цифры и числа до 999
            if (!/^\d{1,3}$/.test(inputValue)) {
                // Очищаем поле ввода от некорректных символов
                target.value = inputValue.replace(/\D/g, '').slice(0, 3); // Ограничиваем ввод до 3 символов
            }
        }

        // Проверяем, что изменения происходят в элементах с id='from' или id='to'
        if (target.id === 'from' || target.id === 'to') {
            var inputValue = parseInt(target.value, 10); // Преобразуем введенное значение в число

            // Проверяем, чтобы введенное значение не превышало размера матрицы
            if (isNaN(inputValue) || inputValue > size - 1) {
                // Если введено число больше размера матрицы, удаляем его
                target.value = ''
            }
        }

    });

    var buttonContainer = document.createElement('div');
    buttonContainer.id = "send-btnContainer"
    buttonContainer.className = 'flex items-center justify-between'; // используем flex для размещения кнопок

    // создание кнопки ввода
    var button = document.createElement('button');
    button.id = 'sendMatrixBtn';
    button.type = 'button';
    button.className = 'text-white bg-gradient-to-r from-green-400 via-green-500 to-green-600 hover:bg-gradient-to-br focus:ring-4 focus:outline-none focus:ring-green-300 dark:focus:ring-green-800 font-medium rounded-lg text-sm px-5 py-2.5 mt-2 text-center' ;
    button.textContent = 'Ввести';
    button.addEventListener('click', function() {
        get_matrix(); // добавление функции get_matrix()
    });

    // создание кнопки очитски
    var clearButton = document.createElement('button');
    clearButton.id = 'clearMatrixBtn';
    clearButton.type = 'button';
    clearButton.className = "text-gray-900 bg-white border border-gray-300 focus:outline-none hover:bg-gray-100 focus:ring-4 focus:ring-gray-200 font-medium rounded-lg text-sm px-5 py-2.5 me-2 mt-2 dark:bg-gray-800 dark:text-white dark:border-gray-600 dark:hover:bg-gray-700 dark:hover:border-gray-600 dark:focus:ring-gray-700" ;
    clearButton.textContent = 'Очистить';
    clearButton.addEventListener('click', function() {
        edit_matrix(); // добавление функции edit_matrix()
    });

    buttonContainer.appendChild(clearButton); // Добавление кнопки "Ввести" в контейнер
    buttonContainer.appendChild(button); // Добавление кнопки "Очистить" в контейнер
    matrixContainer.appendChild(buttonContainer); // Добавление контейнера с кнопками на страницу

    var buttonContainer = document.createElement('div');
    buttonContainer.id = "change-btnContainer"
    buttonContainer.className = 'flex items-center justify-between'; // используем flex для размещения кнопок

    // создание ссылки на результат
    var link = document.createElement('a');
    link.id = 'getResult';
    link.className = 'block text-center font-medium text-blue-600 dark:text-blue-500 hover:underline';
    link.textContent = 'Посмотреть результат';

    var title = document.querySelector('.algorithmTitle'); // получени элемента по имени класса
    link.href = route[title.id]

    // кнопка изменения матрицы
    var changeButton = document.createElement('button');
    changeButton.id = 'changeMatrixBtn';
    changeButton.type = 'button';
    changeButton.className = "text-gray-900 bg-white border border-gray-300 focus:outline-none hover:bg-gray-100 focus:ring-4 focus:ring-gray-200 font-medium rounded-lg text-sm px-5 py-2.5 me-2 mt-2 dark:bg-gray-800 dark:text-white dark:border-gray-600 dark:hover:bg-gray-700 dark:hover:border-gray-600 dark:focus:ring-gray-700" ;
    changeButton.textContent = 'Изменить';
    changeButton.addEventListener('click', function() {
        edit_matrix(false); // добавление функции edit_matrix()
    });

    buttonContainer.appendChild(changeButton); // Добавление кнопки "Ввести" в контейнер
    buttonContainer.appendChild(link); // добавление ссылки на страницу
    buttonContainer.classList.add('hidden')
    matrixContainer.appendChild(buttonContainer); // Добавление контейнера с кнопками на страницу
}


function change_Size(element)
{
    var size = element.value
    document.getElementById('label_size_of_matrix').textContent = `Размер матрицы: ${size}`
}

function set_theme()
{
    if (localStorage.getItem('color-theme') === 'dark' || (!('color-theme' in localStorage) && window.matchMedia('(prefers-color-scheme: dark)').matches)) {
        document.documentElement.classList.add('dark');
        document.getElementById('theme-toggle-light-icon').classList.remove('hidden');
    } else {
        document.documentElement.classList.remove('dark');
        document.getElementById('theme-toggle-dark-icon').classList.remove('hidden');
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
            localStorage.theme = 'dark';
        } else {
            document.documentElement.classList.remove('dark');
            localStorage.setItem('color-theme', 'light');
            localStorage.theme = 'light';
        }

    // if NOT set via local storage previously
    } else {
        if (document.documentElement.classList.contains('dark')) {
            document.documentElement.classList.remove('dark');
            localStorage.setItem('color-theme', 'light');
            localStorage.theme = 'light';
        } else {
            document.documentElement.classList.add('dark');
            localStorage.setItem('color-theme', 'dark');
            localStorage.theme = 'dark';
        }
    }
}