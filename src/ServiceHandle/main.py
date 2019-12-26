from suds.client import Client

url = 'http://10.60.126.248:8098/WebService.asmx?wsdl'
client = Client(url)
# point = 'DCS1_10HAH62CP101_PV'
point = 'DCS1_10HAD14CT201_PV'
startTime = '2019/11/15'
endTime = '2019/12/16'

data  = client.service.GetRealValue(pointID=point)
print(data,'2')