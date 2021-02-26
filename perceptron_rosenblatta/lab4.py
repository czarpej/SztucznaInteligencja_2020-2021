import numpy
from matplotlib import pyplot
from perceptron import *


def part1():
	numpy.random.seed(0)
	m = 1000
	m_half = int(m / 2)
	x1 = numpy.random.rand(m, 1)
	x2_up = numpy.random.rand(m_half, 1) * 0.4 + 0.6
	x2_bottom = numpy.random.rand(m - m_half, 1) * 0.4
	x = numpy.c_[x1, numpy.r_[x2_up, x2_bottom]]
	y = numpy.r_[numpy.ones(m_half), -numpy.ones(m - m_half)].astype("int8")

	# print("x1: ", x1)
	# print("x2_up: ", x2_up)
	# print("x2_bottom: ", x2_bottom)
	# print("x shape:", x.shape)
	# print("x: ", x)

	perceptron = Perceptron()
	w, k = perceptron.fit(x, y)
	print(w, k)

	print(perceptron.predict(x))
	print(perceptron.score(x, y))
	# w0 + w1 * x1 + w2 * x2 = 0
	# x2 = -(w0 + w1 * x1) / x2

	xx = numpy.arange(0, 1+0.01, 0.01)
	yy = -(w[0] + w[1] * xx) / w[2]
	pyplot.plot(xx, yy)
	pyplot.scatter(x[:, 0], x[:, 1], c=y, s=2)
	pyplot.show()


from scipy.spatial.distance import cdist
from matplotlib.pyplot import cm


def part2():
	n = 1000
	m = 100
	x1 = numpy.random.rand(n, 1) * numpy.pi * 2.0
	x2 = numpy.random.rand(n, 1) * 2.0 - 1.0

	x = numpy.c_[x1, x2]
	y = numpy.r_[numpy.abs(numpy.sin(x1)) > numpy.abs(x2)].astype("int8")
	y[y == 0] = -1

	x[:, 0] = (x[:, 0] - numpy.pi)/numpy.pi
	c = numpy.random.rand(m, 2) * 2.0 - 1.0

	sigma = 0.2
	z = numpy.exp(-(cdist(x, c) ** 2)/(2*(sigma ** 2)))
	dist = numpy.c_[numpy.ones(n), z]

	perceptron = Perceptron(k_max=5000)
	w, k = perceptron.fit(dist, y)

	i = 100
	xx1 = numpy.linspace(-1, 1, i)
	xx2 = numpy.linspace(-1, 1, i)
	X1, X2 = numpy.meshgrid(xx1, xx2)

	# print(xx.shape)
	temp = numpy.stack((X1, X2), axis=2)
	# print(temp)
	# print(temp.reshape(i*i, 2))
	distdist = numpy.c_[numpy.ones(i*i), numpy.exp(-(cdist(temp.reshape(i*i, 2), c) ** 2)/(2*(sigma ** 2)))]
	# print("Sum: ", perceptron.predict(distdist).shape)
	# print("Predict: ", perceptron.predict(distdist))
	# print(numpy.stack((X, Y), axis=2))
	# print(X)
	# print(Y)

	# zz = perceptron.predict(xx)
	# print(cdist(numpy.array([[0, 0], [0, 1], [1, 0], [1, 1]]), numpy.array([[0.5, 0.5]])))
	X3 = perceptron.decision_function(distdist).reshape(i, i)
	X3_normalized = perceptron.class_labels[(X3 > 0.0) * 1]
	print("Score: ", perceptron.score(dist, y))

	pyplot.figure()
	pyplot.contourf(X1, X2, X3_normalized.reshape(i, i), cmap=cm.get_cmap("Purples"))
	pyplot.scatter(x[:, 0], x[:, 1], c=y, s=5, cmap=cm.get_cmap("plasma"))
	pyplot.xlabel("x1")
	pyplot.ylabel("x2")
	pyplot.show()

	pyplot.figure()
	pyplot.contourf(X1, X2, X3, cmap=cm.get_cmap("Purples"))
	pyplot.scatter(x[:, 0], x[:, 1], c=y, s=5, cmap=cm.get_cmap("plasma"))
	pyplot.xlabel("x1")
	pyplot.ylabel("x2")
	pyplot.show()

	figure = pyplot.figure()
	axes = figure.gca(projection='3d')
	axes.plot_surface(X1, X2, X3, cmap=cm.get_cmap("plasma"), linewidth=0, antialiased=False)
	axes.set_xlabel("x1")
	axes.set_ylabel("x2")
	axes.set_zlabel("x3")
	pyplot.show()


numpy.random.seed(0)
part2()
