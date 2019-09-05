import airflow.operators
import pkgutil
package = airflow.operators
prefix = package.__name__ + "."
for importer, modname, ispkg in pkgutil.iter_modules(package.__path__, prefix):
    print("Found submodule {} (is a package: {})".format(modname, ispkg))
    module = __import__(modname, fromlist="dummy")
    print("Imported", module)