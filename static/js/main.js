// формирование таблицы
function get_matrix()
{
    var size = document.getElementById('range_size_of_matrix').value // размер матрицы

    // отправка данных для обработки на Python
    fetch('/process', {
        method: 'POST', // тип запроса
        body: size // отправляем данные на сервер
    })

    document.getElementById('matrix_size_div').classList.add('hidden') // прячем кнопку ввода размера матрицы

    var matrixContainer = document.getElementById('matrix_input'); // блок для вставки матрицы
    
    //matrixContainer.innerHTML = ''; // очищаем блок перед созданием новой матрицы

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
        vertexCell.textContent = 'x' + i; // Подписи вершин (строки)
        row.appendChild(vertexCell);

        // Ячейки матрицы для ввода данных (input)
        for (var j = 1; j <= size; j++) {
            var cell = document.createElement('td');
            var input = document.createElement('input');
            input.type = 'text';
            input.name = 'matrixCell' + i + '_' + j;
            cell.appendChild(input);
            row.appendChild(cell);
        }
        tbody.appendChild(row);
    }
    table.appendChild(tbody);
    matrixContainer.appendChild(table);

    // добавление кнопки ввода
    matrixContainer.innerHTML = matrixContainer.innerHTML + '<div><button type="button" class="text-white bg-gradient-to-r from-green-400 via-green-500 to-green-600 hover:bg-gradient-to-br focus:ring-4 focus:outline-none focus:ring-green-300 dark:focus:ring-green-800 font-medium rounded-lg text-sm px-5 py-2.5 text-center me-2 mb-2">Enter</button></div>'
}

    

    // var table = document.createElement('table')
    // // header line
    // table.innerHTML = ''
    // var line = '<tr class="bg-red-900">'
    // for (var i = 0; i <= size; i += 1)
    // {
    //     if (i == 0)
    //     {
    //         line += '<td class="bg-red-900">1</td>'
    //     }
    //     else
    //     {
    //         line += '<td class="bg-grey-500">2</td>'
    //     }
    // }
    // line += '</tr>'
    // // table
    // for (var i = 1; i <= size; i += 1)
    // {
  
    //     line += '<tr>'
    //     for (var j = 0; j <= size; j += 1)
    //     {
    //         if (j == 0)
    //         {
    //             line += '<td class="bg-grey-500">2</td>'
    //         }
    //         else if (i == j)
    //         {
    //             line += '<td class="bg-red-900">1</td>'
    //         }
    //         else
    //         {
    //             line += '<td class="bg-blue-500">3</td>'
    //         }
    //     }
    //     line += '</tr>'
    // }
    // table.innerHTML = '<tbody>' + line + '</tbody>'
    // div_matr.innerHTML = '<div>' + `<table id="matrix_input_table_${size} class="w-full border-separate text-sm text-left rtl:text-right text-gray-500 dark:text-gray-400"` + table.innerHTML + '</table></div>' + div_matr.innerHTML

// Change the icons inside the button based on previous settings

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