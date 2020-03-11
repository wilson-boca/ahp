# coding=UTF-8

from ahp_method import AHP
from matplotlib import pyplot as plt

leader_sample = AHP(
    # method can be approximate, geometric or autovalue
    method='autovalue',
    precision=3,
    alternatives=['Tom', 'Dick', 'Harry'],
    criteria=['Experiência', 'Educação', 'Carisma', 'Idade'],
    sub_criteria={},
    matrice={
        'Experiência': [
            [1, 1 / 4, 4],
            [4, 1, 9],
            [1 / 4, 1 / 9, 1]
        ],
        'Educação': [
            [1, 3, 1 / 5],
            [1 / 3, 1, 1 / 7],
            [5, 7, 1]
        ],
        'Carisma': [
            [1, 5, 9],
            [1 / 5, 1, 4],
            [1 / 9, 1 / 4, 1]
        ],
        'Idade': [
            [1, 1 / 3, 5],
            [3, 1, 9],
            [1 / 5, 1 / 9, 1]
        ],
        'criterios': [
            [1, 4, 3, 7],
            [1 / 4, 1, 1 / 3, 3],
            [1 / 3, 3, 1, 5],
            [1 / 7, 1 / 3, 1 / 5, 1]
        ]
    },
    log=True
)

result = leader_sample.result()
print('\nRanking: {}'.format(result))

plt.bar(result.keys(), result.values())
plt.ylabel('Priority')
plt.show()
