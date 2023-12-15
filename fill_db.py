from app import app, db, Problem_class, Algorithm, Example
app.app_context().push()

db.drop_all()
db.create_all()

kol_problem_class = Problem_class(pr_cl = '<span>Задача нахождения минимального остова</span>', dsc = '''<p>Остовным деревом графа называется дерево, которое можно получить из него путём удаления некоторых рёбер. У графа может существовать несколько остовных деревьев, и чаще всех их достаточно много. <br/> Для взвешенных графов существует понятие веса остовного дерева, которое определено как сумма весов всех рёбер, входящих в остовное дерево. Из него натурально вытекает понятие минимального остовного дерева - остовного дерева с минимальным возможным весом. <br/> Для нахождения минимального остовного дерева графа существуют два основных алгоритма: алгоритм Прима и алгоритм Крускала.</p>''' )
db.session.add(kol_problem_class)
db.session.commit()

kol_algorithm = Algorithm(alg = '<span>Алгоритм Прима</span>', dsc = '''<p>Изначально остов — одна произвольная вершина.<br/> Пока минимальный остов не найден, выбирается ребро минимального веса, исходящее из какой-нибудь вершины текущего остова в вершину, которую мы ещё не добавили. Добавляем это ребро в остов и начинаем заново, пока остов не будет найден.<br/> Таким образом мы можем строить минимальный остов постепенно, добавляя по одному ребра, про которые мы точно знаем, что они минимальные для соединения какого-то разреза.</p>''', pr_cl_id = 1, key = 'pr')
db.session.add(kol_algorithm)
db.session.commit()

kol_algorithm2 = Algorithm(alg = '<span>Алгоритм Краскала <span/>', dsc = '''<p>Механизм, по которому работает данный алгоритм, очень прост. На входе имеется пустой подграф, который и будем достраивать до потенциального минимального остовного дерева. Будем рассматривать только связные графы, в другом случае при применении алгоритма Краскала мы будем получать не минимальное остовное дерево, а просто остовной лес.<br/> Вначале мы производим сортировку рёбер по неубыванию по их весам.<br/> Добавляем i-ое ребро в наш подграф только в том случае, если данное ребро соединяет две разные компоненты связности, одним из которых является наш подграф. То есть, на каждом шаге добавляется минимальное по весу ребро, один конец которого содержится в нашем подграфе, а другой - еще нет.</p>''', pr_cl_id = 1, key = 'kr')
db.session.add(kol_algorithm2)
db.session.commit()

kol_example = Example(ex = "[[0, 20, 20, 17, 22, 18, 32, 30], [0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 14, 0, 23, 0], [0, 0, 0, 0, 0, 8, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 10, 0], [0, 0, 0, 0, 0, 0, 0, 8], [0, 0, 0, 0, 0, 0, 0, 0]]", alg_id = 1)
db.session.add(kol_example)
db.session.commit()

kol_example2= Example(ex = "[[0, 20, 20, 17, 22, 18, 32, 30], [0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 14, 0, 23, 0], [0, 0, 0, 0, 0, 8, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 10, 0], [0, 0, 0, 0, 0, 0, 0, 8], [0, 0, 0, 0, 0, 0, 0, 0]]", alg_id = 2)
db.session.add(kol_example2)
db.session.commit()

and_problem_class = Problem_class(pr_cl = '<span>Задача разбиения графа на компоненты сильной связности</span>', dsc = '''<p> :( </p>''')
db.session.add(and_problem_class)
db.session.commit()

and_algorithm = Algorithm(alg = '<span> Алгоритм Мальгранжа </span>', dsc = '''<p>Алгоритм Мальгранжа предназначен для поиска компонент сильной связности в ориентированном графе и состоит из трёх шагов: <br/> 1. Поиск прямого и обратного транзитивного замыкания для вершины, которая ещё не вошла в одну из компонент сильной связности. <br/> 2. Объединение прямого и обратного транзитивного замыкания будет образовывать новую компоненту сильной связности.<br/> 3. Вершины, которые попали в компоненты сильной связности, больше не рассматриваются для поиска прямого и обратного транзитивного замыкания. Если остались вершины, не вошедшие в компоненты сильной связности, то переход к шагу 1, иначе конец алгоритма. <br/> Полученные объединения прямого и обратного транзитивного замыкания являются компонентами сильной связности. </p>''', pr_cl_id = 2, key = 'ml' )
db.session.add(and_algorithm)
db.session.commit() 
and_algorithm2 = Algorithm(alg = '<span>Алгоритм Косарайю</span>', dsc = '''<p>Алгоритм Косарайю предназначен для поиска компонент сильной связности в ориентированном графе и состоит из трёх шагов: <br/> 1. Выполнить поиск в глубину, пока не будут «помечены» все вершины. Вершина считается «помеченной», когда ей присвоено время выхода из рекурсии поиска в глубину. <br/> 2. Инвертировать исходный граф. <br/> 3. Выполнить поиск в глубину в порядке убывания пометок вершин. <br/> Полученные деревья каждого такта поиска в глубину последнего шага являются компонентами сильной связности. </p>''', pr_cl_id = 2, key = 'ks')
db.session.add(and_algorithm2)
db.session.commit()

and_example = Example(ex = "[ [0, 0, 1, 0, 0, 0], [0, 0, 0, 1, 0, 0], [1, 1, 0, 0, 0, 0], [0, 1, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0], [0, 0, 0, 1, 0, 0] ]", alg_id = 3)
db.session.add(and_example)
db.session.commit()

and_example2= Example(ex = "[ [0, 0, 1, 0, 0, 0], [0, 0, 0, 1, 0, 0], [1, 1, 0, 0, 0, 0], [0, 1, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0], [0, 0, 0, 1, 0, 0] ]", alg_id = 4)
db.session.add(and_example2)
db.session.commit()


kirill_problem_class = Problem_class(pr_cl = '<span>Топологическая сортировка</span>', dsc = '''<p>Топологическая сортировка позволяет упорядочить вершины ориентированного графа в лексикографическом порядке, то есть при продвижении по любому пути орграфа уровень следующей вершины больше уровня предыдущей.</p>''' )
db.session.add(kirill_problem_class)
db.session.commit()

kirill_algorithm = Algorithm(alg = '<span>Алгоритм Демукрона</span>', dsc = '''<p>Алгоритм Демукрона - это алгоритм решения задачи топологической сортировки ориентированного или неориентированного графа.<br/> Алгоритм Демукрона описывается следующим образом:<br/>
сначала k = 0<br/> 1) просматривается столбец матрицы для нахождения вершин без входящих рёбер;<br/> 2) при наличии вершин без входящих рёбер:<br/> &nbsp&nbsp&nbsp а) формируется уровень k, в который помещаются эти вершины;<br/> &nbsp&nbsp&nbsp б) строки вершин сформированного уровня k зануляются в матрице смежности;<br/> &nbsp&nbsp&nbsp в) формируется значение порядковой функции для вершин сформированного уровня k, равное k - номеру уровня;<br/> 3) при отсутствии вершин без входящих рёбер в шаге 2) порядковой функции не существует. Алгоритм прерывается!<br/> 4) алгоритм повторяется с шага 1) для k = k + 1 при наличии вершин, не распределённых по уровням.</p>''', pr_cl_id = 3, key = 'dm')
db.session.add(kirill_algorithm)
db.session.commit()

kirill_algorithm2 = Algorithm(alg = '<span>Метод обхода в глубину<span/>', dsc = '''<p>Поиск в глубину или обход в глубину (англ. Depth-first search, сокращенно DFS) — один из методов обхода графа. К примеру, алгоритм может применяться к ориентированному графу с целью выполнения его топологической сортировки. Сам метод описывается следующим образом: для каждой непройденной вершины необходимо найти все непройденные смежные вершины и повторить поиск для них.<br/> Важно отметить, что граф, к которому применяется данный метод, не должен иметь петель и контуров, иначе поиск в глубину будет бесконечным из-за наличия возможности перехода к уже пройдённым вершинам в процессе поиска.<br/> В процессе обхода вершинам присваивается три роли: непросмотренная/непройденная вершина (синий цвет), просмотренная/пройденная вершина (красный цвет), обработанная вершина/вершина без смежных вершин (зелёный цвет). Каждая найденная в процессе алгоритма обработанная вершина добавляется в стек. Не вершине стека будет находиться вершина 0 уровня, то есть уровни вершин определятся порядком вытаскивания вершин из стека, первая добавленная в стек вершина будет иметь наибольший уровень n-1, где n – количество вершин.<br/> На примере с подробным описанием и графическими представлениями шагов вы можете ознакомиться с работой метода обхода в глубину.</p>''', pr_cl_id = 3, key = 'dfs')
db.session.add(kirill_algorithm2)
db.session.commit() 
kirill_example = Example(ex = "[ [0, 1, 0, 1, 1], [0, 0, 0, 0, 1], [0, 0, 0, 0, 0], [0, 1, 0, 0, 1], [0, 0, 1, 0, 0] ]", alg_id = 5)
db.session.add(kirill_example)
db.session.commit()

kirill_example2= Example(ex = "[ [0, 1, 0, 1, 1], [0, 0, 0, 0, 1], [0, 0, 0, 0, 0], [0, 1, 0, 0, 1], [0, 0, 1, 0, 0] ]", alg_id = 6)
db.session.add(kirill_example2)
db.session.commit() 