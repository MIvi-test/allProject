with open('27_A.txt', 'r', encoding='utf-8') as f:
    data = f.readlines()
    space_of_experience = {}
    all_ID = {}
    space_of_salary = {} # group: [ID; Название_вакансии; Компания;
    #                   Город; Мин_зарплата; Макс_зарплата; 
    #                   Опыт_работы; Дата_публикации; Требуемые_навыки]
    try:
        for i in data[1:]:
            info = i.split(';')
            ID, name, company, city, min_salary, max_salary, experience, publication_date, skills = info
            skip = False
            for j in info:
                if j == '':
                    skip = True
                    break
            if skip == True:
                continue

            avarage_salary = (int('0' + max_salary) + int('0' +min_salary)) / 2 
            all_ID[int(ID)] = info
            x = space_of_salary.get(avarage_salary // 50_000)
            if x == None:
                x = []
            x.append(ID)
            space_of_salary[int(avarage_salary // 50_000)] = x

            y = space_of_experience.get(int(experience)//2+1)
            if y == None:
                y = [ID]
            y.append(ID)
            space_of_experience[int(experience)//2+1] = y         
    except KeyError:
        print("Error", i)
    
    mx = 0
    massive = set()
    transition = 0
    skp = True
    for i in space_of_salary.values():
        for j in i:
            if 'Python' in all_ID[int(i[0])][8]:
                massive.add(int(j))
        mx = max(mx, len(massive) - transition)
    if not skp:
        transition = len(massive)
    print(mx)
    skp = False


    mx = 0
    massive = set()
    transition = 0
    for i in space_of_experience.values():
        for j in i:
            if 'Python'  in all_ID[int(i[0])][8]:
                massive.add(int(j))
        mx = max(mx, len(massive) - transition)
        transition = len(massive)
    if not skp:
        transition = len(massive)
    print(mx)
    skp = False
    
    

    

