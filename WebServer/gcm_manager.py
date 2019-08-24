from pyfcm import FCMNotification

def send_gcm_message(token, message):
	API_KEY = "AAAAHkk70d4:APA91bHDIQEnZYM5NPtOM_daip5KX022O-45NKSsHnRT3Om4TaePfaMHltXCe251to1mlnLpDa8SxdARREW5VMTFNYH3TEOJlp9MztyX4l4Pp2L3PRcu7zyaoMVpFki6rukrIsUpkWLu"
	push_service = FCMNotification(api_key=API_KEY)
	result = push_service.notify_single_device(registration_id=token, message_title="주행 종료", message_body='주행연비 : ' + str(message['fuel_efi']) + 'Km/L, 주행거리 : ' + str(message['distance']) + 'Km') # get json or ditc object

if __name__ == "__main__":
	send_gcm_message("c5oAuBV5ba0:APA91bHsb5TA02dppEyXba545xjU9cK9TC2lo5Rx4vtevdUSVaSr0ETXPblFfEYdSxV3naVhiKWRXoc0COTf_GOcyFQ1xoGbM1C_ACTkdGKfbqmIHXIvUY5CA8yX3ysXSR1ga7ok5Uz_", {'fuel_efi':15.3, 'distance':22.2})
