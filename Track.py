import cv2
import sys
from random import randint
import math

class Track():
  type_tracker = ""
  bboxes = []
  colors = []
  frame_width = 0.0
  camera_distance = 0.0
  focal_distance = 0.0
  field_view = 0.0
  frame_width_m = 0.0
  m_pixel = 0.0
  fact_km_h = 0.0
  frame_time = 0.0
  video_fps = 0.0
  frame_time = 0.0

  def init_parameters(self):
    # Distancia  hacia el objeto en metros
    self.camera_distance = 13.253
    #Distancia foal en metros
    self.focal_distance = 0.0039
    #Campo de vision - Grados
    self.field_view = 69
    #Distancia Horizontal en metros
    self.frame_width_m = round(2*(math.tan(math.radians(self.field_view*0.5))*self.camera_distance),3)
    #Pixel a metros
    self.m_pixel = round(self.frame_width_m/self.frame_width,5)
    #Factor de conversion pixel/metros
    self.fact_km_h = 3600.0
    #Frames por segundo
    self.frame_time = 1000/self.video_fps

  def open_video(self, path):
    #Abrir video
    video = cv2.VideoCapture(path)
    if not video.isOpened():
      print("Error: No se puede abrir el video")
      sys.exit()
    self.frame_width = video.get(cv2.CAP_PROP_FRAME_WIDTH)
    self.video_fps = video.get(cv2.CAP_PROP_FPS)
    return video

  def create_tracker(self):
    #Creación y seleccion del tracker "KFC" Kernelized Correlation Filters
    self.type_tracker = "KCF"
    tracker = cv2.TrackerKCF_create()
    return tracker

  def average_list(self, el_list):
    sum=0.0
    for i in range(0,len(el_list)):
        sum=sum+el_list[i]
    if len(el_list) > 0:
      return sum/len(el_list)
    else:
      return 0

  def simple_tracker(self, path):
    video = self.open_video(path)
    self.init_parameters()
    #Primer frame
    ok, frame = video.read()
    old_frame = frame
    if not ok:
      print('Error: No se puede leer el archivo de video')
      sys.exit()
    #Creacion de punto para el calculo de velocidad instantanea
    feature_params = dict( maxCorners = 100,qualityLevel = 0.3,minDistance = 7,blockSize = 7 )
    lk_params = dict(winSize  = (15,15),maxLevel = 2,criteria = (cv2.TERM_CRITERIA_EPS | cv2.TERM_CRITERIA_COUNT, 10, 0.03))
    old_gray = cv2.cvtColor(old_frame, cv2.COLOR_BGR2GRAY)
    p0 = cv2.goodFeaturesToTrack(old_gray, mask = None, **feature_params)
    tracker = self.create_tracker()
    #Region de delimitacion
    bbox = cv2.selectROI(frame, False)
    #Inicializacion
    ok = tracker.init(frame, bbox)
    velocity_list = []
    while True:
      ok, frame = video.read()
      if not ok:
        break
      frame_gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
      p1, st, err = cv2.calcOpticalFlowPyrLK(old_gray, frame_gray, p0, None, **lk_params)
      good_new = p1[st==1]
      good_old = p0[st==1]
      for i,(new,old) in enumerate(zip(good_new,good_old)):
        a,b = new.ravel()
        c,d = old.ravel()
        if a > bbox[0] and a < (bbox[0]+bbox[2]) and b > bbox[1] and b < (bbox[1]+bbox[3]):
          vel_ins = self.get_velocity_instant(a,b,c,d)
          velocity_list.append(vel_ins)
      vel_ins_average = round(self.average_list(velocity_list),2)
      bbox_old = bbox
      #Actualizacion
      ok, bbox = tracker.update(frame)
      other_vel_ins_average = round(self.get_velocity_instant(bbox_old[0],bbox_old[1],bbox[0],bbox[1]),2)
      if ok:
        #tracking correcto
        p1 = (int(bbox[0]), int(bbox[1]))
        p2 = (int(bbox[0] + bbox[2]), int(bbox[1] + bbox[3]))
        cv2.rectangle(frame, p1, p2, (255,0,0), 2, 1)
      else :
        #tracking incorrecto
        cv2.putText(frame, "Error...", (100,80), cv2.FONT_HERSHEY_SIMPLEX, 0.75,(0,0,255),2)

      # Muestra velocidades en trackeo
      cv2.putText(frame, "Velocidad Tracker" + str(other_vel_ins_average), (100,20), cv2.FONT_HERSHEY_SIMPLEX, 0.75, (50,170,50),2);
      cv2.putText(frame, "Velocidad TK: " + str(vel_ins_average), (100,50), cv2.FONT_HERSHEY_SIMPLEX, 0.75, (50,170,50), 2);
      cv2.imshow("Tracking", frame)
      
      #Para salir presionar ESC
      k = cv2.waitKey(1) & 0xff
      if k == 27 : break
      velocity_list = []

  def get_velocity_instant(self,x1,y1,x2,y2):
    #Distancia Euclidea
    distance = math.sqrt((x2 - x1)**2 + (y2 - y1)**2)
    #Calculo Velocidad Instantanea
    instant_velocity = distance/self.frame_time * self.m_pixel * self.fact_km_h
    return instant_velocity