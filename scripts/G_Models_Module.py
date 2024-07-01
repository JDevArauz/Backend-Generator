class ModelsModule:
    def __init__(self):
        pass
    def generate_setup_models(self, tables):
        """
        Genera el contenido para inicializar todos los modelos y definir las asociaciones.

        Args:
            tables (dict): Diccionario que contiene los nombres de las tablas como claves y listas de definiciones de columnas como valores.

        Returns:
            str: Contenido del archivo index.js que inicializa todos los modelos y define las asociaciones.
        """
        setup_content = ''
        for table_name in tables:
            setup_content += f"const {{ {table_name}, {table_name}Schema }} = require('./{table_name}.model');\n"
        
        setup_content += "\nfunction setupModels(sequelize) {\n"
        
        for table_name in tables:
            setup_content += f"    {table_name}.init({table_name}Schema, {table_name}.config(sequelize));\n"
        
        # Añadir definiciones de asociaciones aquí (si es necesario)

        setup_content += "\n\t//DEFINE YOUR ASSOCIATIONS HERE\n}\n\nmodule.exports = setupModels;\n"

        return setup_content

    def generate_model(self, model_name, columns):
        def data_type_converter(data_type):
            data_type = data_type.lower()
            if 'varchar' in data_type or 'char' in data_type or 'text' in data_type:
                return 'DataTypes.STRING'
            elif 'int' in data_type:
                return 'DataTypes.INTEGER'
            elif 'bigint' in data_type:
                return 'DataTypes.BIGINT'
            elif 'float' in data_type or 'double' in data_type or 'real' in data_type:
                return 'DataTypes.FLOAT'
            elif 'decimal' in data_type or 'numeric' in data_type:
                return 'DataTypes.DECIMAL'
            elif 'date' in data_type:
                return 'DataTypes.DATE'
            elif 'timestamp' in data_type:
                return 'DataTypes.DATE'
            elif 'boolean' in data_type or 'tinyint(1)' in data_type:
                return 'DataTypes.BOOLEAN'
            elif 'json' in data_type:
                return 'DataTypes.JSON'
            elif 'blob' in data_type:
                return 'DataTypes.BLOB'
            else:
                return 'DataTypes.STRING' 
            
        model = f"""
        const {{ Model, DataTypes }} = require('sequelize');
        const sequelize = require('../libs/sequelize');

        const {model_name.upper()}_TABLE = '{model_name}';

        class {model_name} extends Model {{
            
        static associate(models) {{
            // Define associations here if necessary
        }}

        static config(sequelize) {{
            return {{
            sequelize,
            tableName: {model_name.upper()}_TABLE,
            modelName: '{model_name}',
            timestamps: false 
            }}
        }}
        }}

        const {model_name}Schema = {{
        """
        for column in columns:
            column_name, column_type = column
            js_type = data_type_converter(column_type)
            allow_null = 'false' if 'NOT NULL' in column_type.upper() else 'true'

            model += f"""
        {column_name}: {{
            allowNull: {allow_null},
            type: {js_type},
            field: '{column_name}'
        }},
        """
        model = model.rstrip(',\n') + """
        };

        module.exports = {""" f""" {model_name}, {model_name}Schema }};
        """
        return model
    