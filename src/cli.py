import click
from commands.add_command import add_expense
from commands.update_command import update_expense
from commands.delete_command import delete_expense
from commands.list_command import list_expenses
from commands.summary_command import summary


@click.group()
@click.version_option(version="0.7.0", prog_name="Expense Tracker CLI")
def cli():
    pass


# Registering commands
cli.add_command(add_expense, name="add")
cli.add_command(update_expense, name="update")
cli.add_command(delete_expense, name="delete")
cli.add_command(list_expenses, name="list")
cli.add_command(summary, name="summary")


if __name__ == '__main__':
    cli()


# Falta para filtrar gastos por categoria
# Falta para permitir a los usuarios establecer un presupuesto para cada mes
# y mostrar una advertencia cuando el usuario supere el presupuesto
# Falta permitir a los usuarios exportar gastos a un archivo CSV

# Ver si puedo modularizar más el código
# Agregar tests
# Agregar estilos con rich


# Update expense:
# - Comprobar posibles fallos
# - Hacer que lo de actualizar lo que sea del gasto sea opcional y preguntando si está seguro de actualizar
# - Asegurar que tengan las mismas validaciones de los datos en amount, description, category y date
# Lo que ví:
# --- La fecha mejor ver que no reciba una futura que no pasó aún

# Delete expense:
# - Comprobar que todo esté bien
# - posiblemente agregar para borrar por fecha
# --- Por dia en especifico, mes o año
#
# - Lo que ví:
# --- Agregar mensaje de que no se permite id negativos
# --- Agregar validacion para que no agreguen cualquier id
# --- Agregar mensaje de confirmación al querer borrar un gasto por id

# List
# - Comprobar que todo esté bien
# - Le podria agregar que filtre por categoria, fecha o monto especifico (rango de monto)

# Summary
# - Comprobar que todo esté bien
# - Lo que vi:
# --- Al agregar "--year " y un año que no tiene gasto, lanzar solo un mensaje que diga que no se encontró gastos
#     lo que hace ahora es solo lanzar el monto a $0.00, lo mismo si se busca con "--year" y "--month"
# --- Agregar validaciones al poner "--year" asi no pongan numeros negativos o si es posible, fechas futuras que no pasaron
# --- Ver si puedo hacer que "--year" y "--month" al no recibir un número, que comprueben el año o mes actual
# --- Agregar resumen por categoria? también junto con year y month agregados
