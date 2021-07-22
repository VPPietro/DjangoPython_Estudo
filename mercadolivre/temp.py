lista = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14]
n = 6
lista_parcial = []
start = -n
end = n
for i in range(int(len(lista)/n)+1):
    start = start+n
    end = start+n
    lista_parcial.append(lista[start:end])
print(lista_parcial)
