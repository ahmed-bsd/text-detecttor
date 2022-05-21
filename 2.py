import cv2
from pytesseract import Output
import pytesseract
import argparse
import cv2
from gtts import gTTS 
import os 

ap = argparse.ArgumentParser()
ap.add_argument("-i", "--image", 
	help="enter img")
ap.add_argument("-c", "--min-conf", type=int, default=50,
	help="confidence value")
args = vars(ap.parse_args())


camera = cv2.VideoCapture(0)

cv2.namedWindow("test")


while True:
    ret, frame = camera.read()

    if not ret:
        print("no frame")
        break
    cv2.imshow("test", frame)

    k = cv2.waitKey(1)
    if k%256 == 27:
        print("it's closed")
        break
    elif k%256 == 32:
        img_name = "image_cv.png"
        cv2.imwrite(img_name, frame)
        print("{} written!".format(img_name))
        #cam.release()
        break

if not args["image"] :
	image = cv2.imread("image_cv.png")
else :
	
	image = cv2.imread(args["image"])

rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
results = pytesseract.image_to_data(rgb, output_type=Output.DICT)
phrase=""

# loop over each of the individual text localizations
for i in range(0, len(results["text"])):

		x = results["left"][i]
		y = results["top"][i]
		w = results["width"][i]
		h = results["height"][i]
		text = results["text"][i]
		conf = int(results["conf"][i])

		# if confidence value is weak
		if conf > args["min_conf"]:
			# collecting words
			print("Word: {}".format(text)+" => Confidence: {}".format(conf))
			print("")

			# write output on image/frame 
			text = "".join([c if ord(c) < 128 else "" for c in text]).strip()
			cv2.rectangle(image, (x, y), (x + w, y + h), (0, 255, 0), 2)
			cv2.putText(image, text, (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX,
				1, (0, 0, 255), 3)
			
			phrase=phrase+" "+text

			
print(phrase)
if len(phrase) <=1:
		print("nothing to show ... take a clear picture please !")
else:
	   
	   #for sound
		language = 'en'
		output = gTTS(text=phrase, lang=language, slow=False)

		output.save("output.mp3")

		os.system("start output.mp3")
		# display image after detection
		cv2.imshow("Image", image)
		cv2.waitKey(0)


cv2.destroyAllWindows()



