class ServicesModule:
    def __init__(self):
        self.services = []

    def generate_service(self, service_name):
        service = f"""
        const {{ models }} = require('../libs/sequelize');

        class {service_name}Service {{

            constructor() {{}}

            async find() {{
            const res = await models.{service_name}.findAll();
            return res;
            }}

            async findOne(id) {{
            const res = await models.{service_name}.findByPk(id);
            return res;
            }}

            async create(data) {{
            const res = await models.{service_name}.create(data);
            return res;
            }}

            async update(id, data) {{
            const model = await this.findOne(id);
            const res = await model.update(data);
            return res;
            }}

            async delete(id) {{
            const model = await this.findOne(id);
            await model.destroy();
            return {{ deleted: true }};
            }}

        }}

        module.exports = {service_name}Service;
        """
        return service