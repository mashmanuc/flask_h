# from model_ad import delete_tema_test_and_tests, find_temi_by_test, update_test_num_quest
# i=100
# for i in range(1,1200000):
#     try:
#         tems=find_temi_by_test(i)
#         # print(len(tems))

#         zap=((tems[-1].num_quest.split(' ')[0]))+" "

#         if len(tems)==int(tems[-1].num_quest.split(' ')[1]):
#             pass
#         else:
#             for num ,tem in enumerate(tems):
#                 num_z=(zap+str(num+1))
#                 test_id=tem.id
#                 update_test_num_quest(test_id, num_z)

#             print(i)
#     except:
#         print('eror ', i)
#         delete_tema_test_and_tests(i)









# for tem in tems:
#     print(tem.num_quest.split(' ')[1])
