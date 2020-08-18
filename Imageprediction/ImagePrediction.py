from imageai.Prediction import ImagePrediction
import tensorflow as tf

prediction = ImagePrediction()
prediction.setModelTypeAsInceptionV3()
"""
prediction.setModelTypeAsSqueezeNet()
prediction.setModelTypeAsResNet()
prediction.setModelTypeAsInceptionV3()
prediction.setModelTypeAsDenseNet()
"""

prediction.setModelPath("Imageprediction/inception_v3_weights_tf_dim_ordering_tf_kernels.h5")


"""
– parameter prediction_speed (optional) : 
This parameter allows you to reduce the time it takes to predict in an image by up to 80% which leads to slight reduction in accuracy. 

This parameter accepts string values. The available values are “normal”, “fast”, “faster” and “fastest”. The default values is “normal”
"""
prediction.loadModel( prediction_speed = 'normal') 

def predict(): 
	predictions, probabilities = prediction.predictImage("Imageprediction/img.jpg", result_count = 3)
	return predictions, probabilities
	# for eachPrediction, eachProbability in zip(predictions, probabilities):
	#     print(eachPrediction , " : " , eachProbability)



