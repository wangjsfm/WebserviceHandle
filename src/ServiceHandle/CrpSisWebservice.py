from suds.client import Client
from src.conf.AppConf import WebserverUrl
class CrpSisWebApi():
    def __init__(self,url):
        self.client = Client(url)
        self.ArrayOfString = self.client.factory.create('ArrayOfString')

    def ConvertString(self,list,unit):
        """
            将List 数据拼接成
            ['DCS1_10HAH62CP101_PV','DCS1_10HAD14CT201_PV','DCS1_10MW_PV']  格式
        :param list:
        :param unit:
        :return:
        """
        tempList = []
        for index in range(len(list)):
            tempList.append(
                'DCS' + unit + '_' + list[index] + '_PV'
            )
        return  tempList


    def ConverMap(self,arrayOfString,points):
        """
            将标签名称与列表数据一 一 对应起来
            {'10HAH62CP101': -1.7e+308, '20MW': 640.56, '10MW': -1.7e+308}
        :param arrayOfString:
        """
        mapData = {}
        for index in range(len(arrayOfString)):
            mapData[points[index].replace('DCS1_', '', ).replace('_PV', '')] = arrayOfString[index]
        return  mapData

    def GetRealValueList(self,list,unit):
        """
        获取多点实时数据
        将list转为ArrayOfString再发送请求给服务端
        :param list: 传入数组标签【string,】
        :param unit: 机组  ‘1’、‘2’ string格式
        :return:
        """
        tempList = self.ConvertString(list,unit) #格式化 标签

        self.ArrayOfString.string = tempList
        receveData = self.client.service.GetRealValueList(points=self.ArrayOfString)[0] #获取数据为一个字典，取第一个就是所有数据

        return self.ConverMap(receveData,tempList)

    def GetRealValue(self,tagId,unit):
        """
        获取单点 实时数据
        :param tagId:标签名
        :param unit:机组信息
        :return:
        """
        tagName = self.ConvertString(tagId,unit)#返回数组形式
        return self.client.service.GetRealValue(pointID=tagName[0])

    def GetHistValue(self,tagId,startTime,endTime,unit):
        """
        获取单点历史数据
        :param tagId:
        :param startTime:
        :param endTime:
        :param unit:
        :return:   ['2019/12/12 0:00:01,418.20001', '2019/12/12 0:00:25,418.10001', '2019/12/12 0:00:36,418']
        """
        tagName = self.ConvertString(tagId, unit)#返回数组形式
        receveData = self.client.service.GetHistValue(point=tagName[0],startTime= startTime,endTime=endTime)
        return  receveData[0]





if __name__ == '__main__':

    points = ['10HAH62CP101', '10HAD14CT201', '10MW']
    webservice = CrpSisWebApi(WebserverUrl)
    starTime = '2019/12/12'
    endTime = '2019/12/13'
    # data = webservice.GetRealValueList(points,"1")
    # data = webservice.GetRealValue(['20HAD14CT201'],'2')
    data = webservice.GetHistValue(['20HAD14CT201'], starTime,endTime,'2')
    print(data)