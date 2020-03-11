# coding=UTF-8
import numpy as np


class AHP(object):

    def __init__(self, method, precision, alternatives, criteria, sub_criteria, matrice, log=False):
        self.method = method
        self.precision = precision
        self.alternatives = alternatives
        self.criteria = criteria
        self.sub_criteria = sub_criteria
        self.matrice = matrice
        self.log = log
        self.global_priorities = []

    @staticmethod
    def approximate(matrix, precision):
        column_sum = matrix.sum(axis=0)
        norm_matrix = np.divide(matrix, column_sum)
        line_mean = norm_matrix.mean(axis=1)
        return line_mean.round(precision)

    @staticmethod
    def geometric(matrix, precision):
        geo_mean = [np.prod(linha) ** (1 / len(linha)) for linha in matrix]
        norm_geo_mean = geo_mean / sum(geo_mean)
        return norm_geo_mean.round(precision)

    @staticmethod
    def auto_value(matrix, precision, max_iter=100, previous_vector=None):
        square_matrix = np.linalg.matrix_power(matrix, 2)
        line_sum = np.sum(square_matrix, axis=1)
        column_sum = np.sum(line_sum, axis=0)
        actual_vector = np.divide(line_sum, column_sum)

        if previous_vector is None:
            previous_vector = np.zeros(matrix.shape[0])

        difference = np.subtract(actual_vector, previous_vector).round(precision)
        if not np.any(difference):
            return actual_vector.round(precision)

        max_iter -= 1
        if max_iter > 0:
            return AHP.auto_value(square_matrix, precision, max_iter, actual_vector)
        else:
            return actual_vector.round(precision)

    @staticmethod
    def consistency(matrix):
        if matrix.shape[0] and matrix.shape[1] > 2:
            lambda_max = np.real(np.linalg.eigvals(matrix).max())
            ic = (lambda_max - len(matrix)) / (len(matrix) - 1)
            ri = {3: 0.52, 4: 0.89, 5: 1.11, 6: 1.25, 7: 1.35, 8: 1.40, 9: 1.45,
                  10: 1.49, 11: 1.52, 12: 1.54, 13: 1.56, 14: 1.58, 15: 1.59}
            rc = ic / ri[len(matrix)]
        else:
            lambda_max = 0
            ic = 0
            rc = 0

        return lambda_max, ic, rc

    def local_priority_vector(self):
        local_priority_vector = {}
        for criterion in self.matrice:
            matriz = np.array(self.matrice[criterion])
            if self.method == 'approximate':
                local_priorities = self.approximate(matriz, self.precision)
            elif self.method == 'geometric':
                local_priorities = self.geometric(matriz, self.precision)
            else:
                if matriz.shape[0] and matriz.shape[1] >= 2:
                    local_priorities = self.auto_value(matriz, self.precision)
                else:
                    local_priorities = self.approximate(matriz, self.precision)

            local_priority_vector[criterion] = local_priorities

            lambda_max, ic, rc = self.consistency(matriz)

            if self.log:
                print('\nPrioridades locais do critério ' + criterion + ':\n', local_priorities)
                print('Soma: ', np.round(np.sum(local_priorities), self.precision))
                print('Lambda_max = ', lambda_max)
                print('Ìndice de consistência ' + criterion + ' = ', round(ic, self.precision))
                print('Razão de consistência ' + criterion + ' = ', round(rc, 2))

        return local_priority_vector

    def global_priority_vector(self, priorities, weights, criteria):
        for criterion in criteria:
            weight = weights[criteria.index(criterion)]
            local_priorities = priorities[criterion]
            global_piority = np.round(weight * local_priorities, self.precision)

            if criterion in self.sub_criteria:
                self.global_priority_vector(priorities, global_piority, self.sub_criteria[criterion])
            else:
                self.global_priorities.append(global_piority)

                if self.log:
                    print('\nPrioridades globais do criterio ' + criterion + '\n', global_piority)
                    print('Soma: ', sum(global_piority).round(self.precision))

    def result(self):
        priorities = self.local_priority_vector()
        self.global_priority_vector(priorities, priorities['criterios'], self.criteria)
        priorities = np.array(self.global_priorities)
        priorities = priorities.sum(axis=0).round(self.precision)
        return dict(zip(self.alternatives, priorities))
