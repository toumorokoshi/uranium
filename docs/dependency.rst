===========================
Declaring Task Dependencies
===========================

----------------
Prepending Tasks
----------------

Uranium provides a declarative task dependency system
through task_requires::

    from uranium import task_requires

    def main(build):
        print("main was")

    # this ensures main is run first, during
    # an execution.
    @task_requires("main")
    def test(build):
        print("test was run")

    # a list can be passed in. In that case,
    # each dependency is executed in the order
    # it appears in the list.
    #
    # notice that a string with the task name,
    # or the task itself can be passed in.
    @task_requires(["main", test])
    def build_docs(build):
        print("main was")


This relationship can be created after the fact by add_requires::

    # test requires main
    build.tasks.prepend("test", "main")

--------------------------------------
Executing Tasks After an Existing Task
--------------------------------------

.. code:: python

   # ensures test executes after main
   build.tasks.append("main", "test")
