import requests

BASE_URL = "https://api-colombia.com/api/v1/TypicalDish"


def dish_fetch(num):
    try:
        url = f"{BASE_URL}/{num}"
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException:
        return None


def obtener_todos_los_platos():
    try:
        response = requests.get(BASE_URL, timeout=10)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"❌ Error al conectar con la API: {e}")
        return None


def obtener_departamentos_disponibles(platos):
    departamentos = set()
    for plato in platos:
        departamento = plato.get('department') or {}
        nombre = departamento.get('name')
        if nombre:
            departamentos.add(nombre)
    return sorted(departamentos)


def construir_codigo_dane(departamento):
    try:
        id_depto = int(departamento.get('id', 0))
        municipios = int(departamento.get('municipalities', 0))
        return f"{id_depto:02d}{municipios:03d}"
    except (ValueError, TypeError):
        return "No disponible"


def filtrar_por_nombre(platos, palabra_clave):
    resultados = []
    for plato in platos:
        if palabra_clave.lower() in plato.get('name', '').lower():
            resultados.append(plato)
    return resultados


def filtrar_por_ingrediente(platos, ingrediente):
    resultados = []
    for plato in platos:
        ingredientes = plato.get('ingredients', '').lower()
        if ingrediente.lower() in ingredientes:
            resultados.append(plato)
    return resultados


def filtrar_por_departamento(platos, nombre_departamento):
    resultados = []
    for plato in platos:
        departamento = plato.get('department') or {}
        if nombre_departamento.lower() in departamento.get('name', '').lower():
            resultados.append(plato)
    return resultados


def mostrar_plato(plato):
    print("\n" + "=" * 10)
    print(f"🍽️  {plato.get('name', 'Nombre no disponible')}")
    print("-" * 10)
    print(f"📌 ID: {plato.get('id', 'No disponible')}")
    print(f"📝 Descripción: {plato.get('description', 'No disponible')}")
    print(f"🥘 Ingredientes: {plato.get('ingredients', 'No disponibles')}")
    print(f"🖼️  Imagen: {plato.get('imageUrl', 'No disponible')}")
    departamento = plato.get('department') or {}
    print(f"📍 Departamento: {departamento.get('name', 'No disponible')}")
    print(f"🔢 Código DANE: {construir_codigo_dane(departamento)}")
    print("=" * 10)


def mostrar_menu():
    print("\n" + "=" * 10)
    print("🇨🇴  BUSCADOR DE PLATOS TÍPICOS DE COLOMBIA  🇨🇴".center(50))
    print("=" * 10)
    print("1. Buscar por Nombre de Plato")
    print("2. Buscar por Ingrediente")
    print("3. Buscar por Departamento")
    print("4. Salir")
    print("=" * 10)


def mostrar_opciones_numeradas(titulo, opciones):
    print(f"\n📋 {titulo} disponibles ({len(opciones)}):")
    print("-" * 10)
    for i, opcion in enumerate(opciones, start=1):
        print(f"  {i}. {opcion}")
    print("-" * 10)


def seleccionar_departamento(departamentos_disponibles):
    mostrar_opciones_numeradas("Departamentos", departamentos_disponibles)
    print("\n💡 Puede escribir el NÚMERO del departamento o parte de su NOMBRE (mínimo 3 letras).")
    entrada = input("Ingrese el número o el nombre del departamento: ").strip()

    if entrada.isdigit():
        indice = int(entrada)
        if 1 <= indice <= len(departamentos_disponibles):
            return departamentos_disponibles[indice - 1]
        else:
            print("❌ El número ingresado no está en la lista.")
            return ""
    elif len(entrada) >= 3:
        return entrada
    else:
        print("❌ Debe ingresar al menos 3 letras para realizar la búsqueda.")
        return ""


def main():
    print("¡Bienvenido al buscador gastronómico de Colombia!")
    print("\n⏳ Descargando información de la API...")

    todos_los_platos = obtener_todos_los_platos()
    if not todos_los_platos:
        print("No se pudo cargar la información. Saliendo del programa.")
        return

    print(f"✅ ¡Se cargaron {len(todos_los_platos)} platos típicos!")

    departamentos_disponibles = obtener_departamentos_disponibles(todos_los_platos)

    while True:
        mostrar_menu()
        opcion = input("Seleccione una opción (1-4): ").strip()

        if opcion == "4":
            print("\n¡Gracias por usar el buscador! Saliendo...")
            break

        resultados = []
        termino = ""

        if opcion == "1":
            print("\n💡 Escriba parte del nombre del plato (mínimo 3 letras).")
            print("   Ejemplos: Bandeja, Ajiaco, Sancocho, Lechona, Arepa...")
            termino = input("Ingrese el nombre del plato: ").strip()
            if len(termino) < 3:
                print("❌ Debe ingresar al menos 3 letras para realizar la búsqueda.")
                continue
            resultados = filtrar_por_nombre(todos_los_platos, termino)

        elif opcion == "2":
            print("\n💡 Escriba parte del nombre del ingrediente (mínimo 3 letras).")
            print("   Ejemplos: arroz, frijoles, carne, pollo, maíz...")
            termino = input("Ingrese el ingrediente: ").strip()
            if len(termino) < 3:
                print("❌ Debe ingresar al menos 3 letras para realizar la búsqueda.")
                continue
            resultados = filtrar_por_ingrediente(todos_los_platos, termino)

        elif opcion == "3":
            termino = seleccionar_departamento(departamentos_disponibles)
            if not termino:
                continue
            resultados = filtrar_por_departamento(todos_los_platos, termino)

        else:
            print("❌ Opción no válida. Intente de nuevo.")
            continue

        if resultados:
            print(f"\n🔍 Se encontraron {len(resultados)} plato(s) para '{termino}':")
            for plato in resultados:
                mostrar_plato(plato)
        else:
            print(f"\n😕 No se encontraron platos para '{termino}'.")


if __name__ == "__main__":
    main()