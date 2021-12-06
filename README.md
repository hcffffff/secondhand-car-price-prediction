# secondhand-car-price-prediction

## 开题报告
1. 题目（初步）：基于[天池的二手车价格预测](https://tianchi.aliyun.com/competition/entrance/231784/introduction)做出的创新与思考。
2. 理解：虽然二手车价格一直是一个常被提起的问题，但是近几年随着国家政策的出台，各种新能源汽车抢占传统汽油车市场，以及不同地区（尤其是针对中国本土）的二手车价格是否会有较大差别（由于政策、收入等因素的影响）。对比国产新能源汽车与外企的新能源车的二手车价格。
3. 创新点：
    1. 以往的二手车价格预测几乎都是汽油车，没有对于新能源车的价格预测。
    2. 对于天池数据平台的数据，进行一个数据分析
        ```
        0.0    91656
        1.0    46991
        2.0     2212
        3.0      262
        4.0      118
        5.0       45
        6.0       36
        Name: fuelType, dtype: int64
        ```
        对于燃料种类为电动（fuelType = 6）的车其实只占到了36/150000，训练样本太少，所以数据可能不太适合，可能需要重新在二手车平台（尤其是中国的）上爬取数据。
    3. 对于不同城市的电动车价格做出不同的预测。
    4. 实现一个可以交互的二手车价格评估预测平台。
4. 官方baseline模型已在`\dataset\tianchi_dataset\dataset-baseline-model.ipynb`中给出。
5. 文献阅读总结：
   1. 基于深度学习的二手车价格预测模型及影响分析：
      1. 基于深度神经网络（DNN）模型，采用控制变量法分析交易价格影响因素的重要程度。指导价、使用时间、行驶距离、省份和汽车品牌的重要性分别占67%、13.06%、9.08%、6.22%和4.64%。
      2. 现有的二手车市场交易研究可分为：（1）二手车价值评估，包括影响因素、评估模型、评估应用 等研究。（2）二手车预测， 包括保值率预测、销量预测等研究。
   2. Second Hand Price Prediction for Tesla Vehicles
      1. 针对特斯拉的汽车研究了不同的机器学习技术，如决策树、支持向量机 (SVM)、随机森林和深度学习，并最终通过增强决策树回归实现。
      2. 实现了一个可以预测Tesla汽车价格的网络服务。
6. Baseline：
   1. [采用lightgbm+catboost+neural_network](https://github.com/wujiekd/Predicting-used-car-prices)
   2. [采用LGB+XGBoost](https://github.com/WillianWang2025/UsedCarPricePrediction/blob/master/LGB_and_XGBoost.ipynb)
7. 待办：
   + 初步研究框架+算法确定
   + 数据集的获取