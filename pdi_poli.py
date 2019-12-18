from colorama import Fore, Style
import os, re, shutil, img2pdf
from PIL import Image, ImageFilter


numbers = re.compile(r'(\d+)') #coloca ordenadamente os arquivos do diretorio

def numericalSort(value):
#Função que ordenará para que as imagens saiam na ordem que foram digitalizadas

   parts = numbers.split(value)
   parts[1::2] = map(int, parts[1::2])
   return parts

def renomear(directory):
#Função que renomeia os arquivos para melhor manipulação

	i=0
	diretorio = directory
	for nome in sorted(os.listdir(diretorio), key = numericalSort):
		new_name = "impressao"+str(i)+".tif"
		src = diretorio+nome
		new_name=diretorio+new_name
		os.rename(src, new_name)
		i+=1

def apresentacao():
#Função de apresentação do conteúdo
   print(" ")
   print(" ")
   print("-------------------------------------")
   print("Universidade de Pernambuco")
   print("Processamento Digital de Imagens")
   print("Professores: Paulo Hugo e Lylian Gomes")
   print("Programa realizado pelos alunos de Telecom")
   print("--------------====------------------")
   print(" ")
   print(" ")
   print("O programa a seguir pega imagens de TCC's digitalizados e melhora sua qualidade visual, para uma melhor apresentação")
   print(" ")
   print(" ")
   
apresentacao()
diretorio = input("Digite o caminho das imagens: ")
print(" ")
print("O diretório escolhido é: " + Fore.RED + diretorio)
renomear(diretorio)
current_path = diretorio
'''
Nesta parte estamos convertendo o .tif para .jpg
'''
for root, dirs, files in os.walk(current_path, topdown=False):
   for name in files:
      print(os.path.join(root, name))
        #caso os.path.splitext(os.path.join(root, name))[1].lower() == ".tiff":
      if os.path.splitext(os.path.join(root, name))[1].lower() == ".tif":
         if os.path.isfile(os.path.splitext(os.path.join(root, name))[0] + ".jpg"):
            print ("A jpeg file already exists for {0}".format(name))
            # Se um jpeg com mesmo nome NÃO exista, converte um do .tif
         else:      
            outputfile = os.path.splitext(os.path.join(root, name))[0] + ".jpg"
            try:
               im = Image.open(os.path.join(root, name))
               print ("Convertendo jpeg para {0}".format(name))
               im.thumbnail(im.size)
               im.save(outputfile, "JPEG", quality=100)
            except Exception as e:
               print (e)
'''
Logo após estamos criando a pasta de resultados
'''
files_fold = os.listdir(current_path)
pasta_backup = "Resultados_jpeg"
arquivos_resultantes = os.path.join(current_path, pasta_backup)
try:
	os.mkdir(arquivos_resultantes)
except OSError:
	print("Falha ao criar diretorio.")
else:
	print("Diretorio criado com sucesso")

for item in files_fold:
	if item.endswith(".jpg"):
		shutil.move(os.path.join(current_path,item), os.path.join(arquivos_resultantes,item))
		print ("Movendo {0}".format(item))

'''
A partir daqui começa o processamento da imagem a função é trabalhada
para ser binarizada e filtrada
'''
dirs = os.listdir(current_path+pasta_backup+'/')
for item in dirs:
	if os.path.isfile(current_path+pasta_backup+'/'+item):
		imagem1=Image.open(current_path+pasta_backup+'/'+item)
		print("Binarizando e  filtrando "+imagem1.filename)
		name,extension = os.path.splitext(current_path+pasta_backup+'/'+item)
		imagem_filtrada=imagem1.filter(ImageFilter.DETAIL)
		imagem_filtrada_binarizada=imagem_filtrada.convert('1')
		imagem_filtrada_binarizada.save(name+'final'+extension)

os.chdir(current_path+pasta_backup+'/')

'''
Logo após é convertida para pdf
'''
print("Convertendo para PDF...")
with open("resultadofinal.pdf", "wb") as f:
   
   f.write(img2pdf.convert([i
   for i in sorted(os.listdir(os.getcwd()), key = numericalSort) 
     if i.endswith("final.jpg")]))
   for  i in sorted(os.listdir(os.getcwd()), key = numericalSort):
      if i.endswith("final.jpg"):
         print("Convertendo "+i)
print("Arquivo criado com sucesso")
print(" ")
print("FIM")
print("------------------------------------------------")

			
