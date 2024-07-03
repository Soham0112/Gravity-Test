import numpy as np

def nor_tang(vector1,vector2):
    sub_vec=np.subtract(vector2,vector1)
    unit_norm=sub_vec/np.linalg.norm(sub_vec)

    unit_tang=np.array([-unit_norm[1],unit_norm[0]])

    return unit_norm,unit_tang

vel_1=np.array([1,2])
vel_2=np.array([3,4])

norm_vec,tang_vec=nor_tang(vel_1,vel_2)
# print(norm_vec,tang_vec)

print(vel_1*3)


