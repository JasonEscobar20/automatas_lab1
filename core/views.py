from django.shortcuts import render


# Create your views here.
def index_view(request):

    return render(request, 'core/index.html')

def get_content(line):
    content = line
    print('entra acsa')

    if '{' in line:
        first_square_bracket_index = line.index('{') + 1
        content = line[first_square_bracket_index: -1]
        content = content.replace('}', '')

        content = content.split(',') if 'W=' not in line else content
    else:
        equals_index = line.index('=') + 1
        content = line[equals_index:]

    return content

def get_transition_list(line, quintupla, alphabet):
    transition_list = []
    test = []


    split_transition = line.split('),')
    
    for item in split_transition:
        remove_parenthesis = item.replace('(', '').replace(')', '')
        transition_list.append(remove_parenthesis.split(','))

    pruebas = []

    for index, value in enumerate(quintupla):
        state = value
        pruebas.append([state])
        test_1 = {}

        for item in transition_list:
            state_to_evaluate = item[0]
            letter = item [1]
            result_state = item[2]
            verify = test_1.get(letter, 0)
            if verify == 0:
                test_1[letter] = []
            

            if state == state_to_evaluate:
                test_1[letter].append(result_state)

        pruebas[index].append(test_1.items())
    
    return pruebas

def read_txt(request):
    get_data = request.POST
    get_file = request.FILES['filename']
        
    test = [line.rstrip() for line in get_file]
    data = {}
    txt_lines = []
    quintupla = []

    for line in test:
        decode_line = line.decode()
        txt_lines.append(decode_line)

        if 'Q=' in decode_line:
            quintupla = get_content(decode_line)
            quintupla = quintupla
            data['quintupla'] = quintupla
            continue
        if 'F=' in decode_line:
            alphabet = get_content(decode_line)
            data['alphabet'] = alphabet
            continue
        if 'i=' in decode_line:
            initial_state = get_content(decode_line)
            data['initial_state'] = initial_state
            continue
        if 'A=' in decode_line:
            success_state = get_content(decode_line)
            data['success_state'] = success_state
            continue
        if 'W=' in decode_line:
            transition = get_content(decode_line)
            transition_array = get_transition_list(transition, quintupla, alphabet)
            data['transition_array'] = transition_array
            # print(transition_array)
            continue
            


    return render(request, 'core/index.html', {
        'txt_lines': txt_lines,
        'data': data
    })