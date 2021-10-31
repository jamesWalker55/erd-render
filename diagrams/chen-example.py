from modules.render import ObjGraph

graph = ObjGraph("chen-custom", engine="neato")

# create entity nodes
graph.node_style(shape="box")
course = graph.node("course")
institute = graph.node("institute")
student = graph.node("student")

# create property nodes
graph.node_style(shape="ellipse")
name1 = graph.node("<X<SUB>1</SUB><SUP>(1)</SUP>>")
name2 = graph.node("na  me")
name3 = graph.node("name")
code = graph.node("code")
grade = graph.node("grade")
number = graph.node("number")

# create relation nodes
graph.node_style(shape="diamond")
c_i = graph.node("C-I")
s_c = graph.node("S-C")
s_i = graph.node("S-I")

graph.edge(name1, course)
graph.edge(code, course)
graph.edge(course, c_i, label="n")
graph.edge(c_i, institute, label="1")
graph.edge(institute, name2)
graph.edge(institute, s_i, label="1")
graph.edge(s_i, student, label="n")
graph.edge(student, grade)
graph.edge(student, name3)
graph.edge(student, number)
graph.edge(student, s_c, label="m")
graph.edge(s_c, course, label="n")

graph.view()
