from glob import glob


numero_de_linhas = 0

def document_in_list_of_directories(document, directories):
    check = False
    for directory in directories:
        if directory in document:
            check = True

    return check

LIBS = ['count.py']

DOT_FOLDERS = ['.mypy_cache', '.venv', '__pycache__',
            'worker_rmq', 'worker_loop', 'site', 'tests']

def contar_linhas(documento: str) -> int:
    with open(documento) as f:
        content = f.readlines()
        content = [line.strip() for line in content if line.strip() != '']
        len_content = len(content)
    return len_content


FORMATOS = ['html', 'css', 'js', 'py', 'yml',
            'conf', 'dockerfile', 'sql']

GLOBS = [
    glob(f'**/*.{formato}', recursive=True)
    for formato in FORMATOS
]
dic = {}
last = None

for GLOB in GLOBS:
    try:
        formato = GLOB[0].split('.')[-1]
        n = 0
        if GLOB:
            for i, documento in enumerate(GLOB):
                if not document_in_list_of_directories(documento, DOT_FOLDERS):
                    if (documento not in LIBS and
                        not documento.startswith('tests')):
                        
                        numero_de_linhas += contar_linhas(documento)
                        n += contar_linhas(documento)
        dic[formato] = n
    except IndexError:
        pass
        

print(f"O número total de linhas em todos os arquivos é {numero_de_linhas}.")