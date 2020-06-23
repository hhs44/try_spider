

import jieba
from collections import Counter

test_text = "《百年孤独》，是哥伦比亚作家加西亚·马尔克斯创作的长篇小说，" \
            "是其代表作，也是拉丁美洲魔幻现实主义文学的代表作，" \
            "被誉为“再现拉丁美洲历史社会图景的鸿篇巨著”。" \
            "作品描写了布恩迪亚家族七代人的传奇故事，以及加勒比海" \
            "沿岸小镇马孔多的百年兴衰，反映了拉丁美洲一个世纪以来风云变幻的历史" \
            "。作品融入神话传说、民间故事、宗教典故等神秘因素，巧妙地糅合了现实与虚幻，" \
            "展现出一个瑰丽的想象世界，成为20世纪重要的经典文学巨著之一。"
seg_list = jieba.cut(test_text, cut_all=True)
# print("Full Mode:" + "/".join(seg_list))
# text_list = list(seg_list)
# print(text_list)
# seg = Counter(test_text)
# print(seg)

import wordcloud
w = wordcloud.WordCloud()
w.generate('and that government of the people, by the people, for the people, shall not perish from the earth.')
w.to_file('output1.png')
