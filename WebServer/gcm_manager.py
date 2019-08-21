from pyfcm import FCMNotification

def send_gcm_message(token, message):
	API_KEY = "AAAAHkk70d4:APA91bHDIQEnZYM5NPtOM_daip5KX022O-45NKSsHnRT3Om4TaePfaMHltXCe251to1mlnLpDa8SxdARREW5VMTFNYH3TEOJlp9MztyX4l4Pp2L3PRcu7zyaoMVpFki6rukrIsUpkWLu"
	push_service = FCMNotification(api_key=API_KEY)
	result = push_service.notify_single_device(	registration_id=token, message_title="주행 종료", message_body=message) # get json or ditc object

if __name__ == "__main__":
	send_gcm_message("eEjUpeFccz8:APA91bFm_QE2CFtVVmPbbcHQiRR4j7Smt7Nunleq9u9cPChaA4w4bbnbfVw-YEwTRZD9MZHoaGQbmowQQp4egglrhB6Wy1mI32JCBbMhPYTcP75EZKiL57KjCAJrcrjs8y71uQ4QYpFu", {'fuel_efi':15.3, 'distance':22.2})
