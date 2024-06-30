from G_Controllers_Module import ControllersModule as controller
from G_Routers_Module import RoutersModule as router
from G_Services_Module import ServicesModule as service
from G_Models_Module import ModelsModule as model
from G_DBConfig_Module import DBConfigModule as dbconfig
import re
import os

class Main:
    """
    Esta clase representa la funcionalidad principal del programa.
    Proporciona métodos para analizar un archivo SQL, crear directorios
    y generar archivos de modelo, controlador, servicio y enrutador basados en las tablas SQL analizadas.
    """

    def __init__(self):
        pass
    
    def parse_sql(self, sql_file_path):
        """
        Analiza un archivo SQL y extrae la información de las tablas y columnas.

        Args:
            sql_file_path (str): La ruta al archivo SQL.

        Returns:
            dict: Un diccionario que contiene los nombres de las tablas como claves y una lista de definiciones de columnas como valores.
                  Cada definición de columna es una tupla que contiene el nombre de la columna y el tipo.
        """
        sql_content = ''
        columns = ''
        table = ''
        write = False
        try:
            with open(sql_file_path, 'r', encoding='utf-8') as file:
                sql_content = file.readlines()
        except FileNotFoundError:
            print(f"Error: No se encontró el archivo '{sql_file_path}'.")
            return {}
        
        
        column_pattern = re.compile(r'`(\w+)` (\w+(\(\d+\))?)', re.IGNORECASE)
        tables_dict = {}
        for line in sql_content:
            if ';\n' in line and write:
                write = False
                columns += line  
                columns_definitions = []
                for column_match in column_pattern.finditer(columns):
                    column_name = column_match.group(1)
                    column_type = column_match.group(2)
                    columns_definitions.append((column_name, column_type))
                tables_dict[table] = columns_definitions
                columns = ''
            if 'CREATE TABLE' in line:
                write = True
                table = re.compile(r'`(\w+)`').findall(line)[0]  # Extrae el nombre de la tabla
                continue
            if write:
                columns += line
        print(f"Tablas encontradas: {list(tables_dict.keys())}") 
        print(f"Número de tablas encontradas: {len(tables_dict)}")
        return tables_dict

    def create_directories(self):
        """
        Crea los directorios necesarios para almacenar los archivos generados.
        """
        directories = ['backend/models', 'backend/controllers', 'backend/services', 'backend/routes', 'backend/config', 'backend/libs']
        for directory in directories:
            if not os.path.exists(directory):
                os.makedirs(directory)

    def main(self):
        """
        Punto de entrada principal del programa.
        Analiza el archivo SQL, genera archivos de modelo, controlador, servicio y enrutador,
        y los guarda en los directorios correspondientes.
        """
        sql_file_path = 'SELECT YOUR SQL PATH'  # Reemplaza esto con la ruta a tu archivo SQL
        tables = self.parse_sql(sql_file_path)

        if not tables:
            print("No se encontraron tablas en el archivo SQL.")
            return

        self.create_directories()

        for table_name, columns in tables.items():
            model_content = model.generate_model(self, table_name, columns)
            controller_content = controller.generate_controller(self, table_name)
            service_content = service.generate_service(self, table_name)
            router_content = router.generate_router(self, table_name)
            
            model_file_path = f'backend/models/{table_name}.model.js'
            controller_file_path = f'backend/controllers/{table_name}.controller.js'
            service_file_path = f'backend/services/{table_name}.service.js'
            router_file_path = f'backend/routes/{table_name}.router.js'
            
            with open(model_file_path, 'w', encoding='utf-8') as model_file:
                model_file.write(model_content)
            print(f"Archivo de modelo generado: {model_file_path}")
            
            with open(controller_file_path, 'w', encoding='utf-8') as controller_file:
                controller_file.write(controller_content)
            print(f"Archivo de controlador generado: {controller_file_path}")
            
            with open(service_file_path, 'w', encoding='utf-8') as service_file:
                service_file.write(service_content)
            print(f"Archivo de servicio generado: {service_file_path}")
            
            with open(router_file_path, 'w', encoding='utf-8') as router_file:
                router_file.write(router_content)
            print(f"Archivo de enrutador generado: {router_file_path}")
            
        # PATHS FOR CONFIGURATION FILES
        models_index_file_path = 'backend/models/index.js'
        routes_index_file_path = 'backend/routes/index.js' 
        app_file_path = 'backend/index.js'
        env_file_path = 'backend/.env'
        config_file_path = 'backend/config/config.js'
        libs_file_path = 'backend/libs/sequelize.js'
        
        setup_content = model.generate_setup_models(self, tables)
        with open(models_index_file_path, 'w', encoding='utf-8') as index_file:
            index_file.write(setup_content)
        print(f"Archivo Models index.js generado en: {models_index_file_path}")
        
        with open(routes_index_file_path, 'w', encoding='utf-8') as index_file:
            index_file.write(router.generate_index_router(self))
        print(f"Archivo Routes index.js generado en: {routes_index_file_path}")
        
        with open(app_file_path, 'w', encoding='utf-8') as app_file:
            app_file.write(dbconfig.generate_index(self))
            print(f"Archivo index.js generado en: {app_file_path}")
            
        with open(env_file_path, 'w', encoding='utf-8') as env_file:
            env_file.write(dbconfig.generate_env(self))
            print(f"Archivo .env generado en: {env_file_path}")
            
        with open(config_file_path, 'w', encoding='utf-8') as config_file:
            config_file.write(dbconfig.generate_config(self))
            print(f"Archivo config.js generado en: {config_file_path}")
            
        with open(libs_file_path, 'w', encoding='utf-8') as libs_file:
            libs_file.write(dbconfig.generate_sequelize_config(self))
            print(f"Archivo sequelize.js generado en: {libs_file_path}")
        
        with open('backend/package.json', 'w', encoding='utf-8') as package_file:
            package_file.write(dbconfig.generate_package(self))
            print("Archivo package.json generado en: backend/package.json")
            
        print("BACKEND GENERADO CON ÉXITO.")
        

if __name__ == '__main__':
    app = Main()
    app.main()
