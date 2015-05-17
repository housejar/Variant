# -*- coding: utf-8 -*-
# Filename: mymodule.py
#
#图像输出~~~各种输出~~
#
from Gorilla.gorilla import *

class PlotHist(GorilaBasis):
    """docstring for PlotHist"""
    plot_Type = 'SL'
    plot_Title = 'Group'

    #存放路径
    plot_Path = 'd:/TestData/vlogic/u/'
    #这个东西可以有更好的方法来整
    mask = np.array([
        [1,0,1,0],
        [1,0,1,1],
        [1,0,0,0],
        [1,0,0,1], 
        [1,1,1,0],
        [1,1,1,1],
        [1,1,0,0],
        [1,1,0,1],
        [0,0,1,0],
        [0,0,1,1],
        [0,0,0,0],
        [0,0,0,1],
        [0,1,1,0],
        [0,1,1,1],
        [0,1,0,0],
        [0,1,0,1]])
    fn_std = ['f0','f1','f2','f3',
          'f4','f5','f6','f7',
          'f8','f9','f10','f11',
          'f12','f13','f14','f15']
    fn_will_be_used = ['f0','f1','f2','f3',
          'f4','f5','f6','f7',
          'f8','f9','f10','f11',
          'f12','f13','f14','f15']
    
     
    def __init__(self):
        super(PlotHist,self).__init__()


    #返回一个文件名
    def _getFileName(self,N,n,power = 1,GroupType='SL',mod1='G',mod2='P',mod3='D',opcode='0000'):
       # +time.strftime('%Y-%m-%d-%H-%M-%S',time.localtime(time.time()))
        return GroupType.upper()+'-Group_'+'N='+str(N)+'_'+'n='+str(n)+'M='+str(power)+'_'+mod2+'_'+opcode+'__'+'.png'

    def _setOutPutPath(self,outPutPath):
        self.plot_Path = outPutPath

    def _initOutPutPath(self):
        """初始化存放结果的路径"""
        
        

    def _plot_sl(self,N,mask,title,power=1,operation="1122"):
        """
        """
        result = np.array(super(PlotHist,self).createBasis(N,power,operation))
        ploty = {}
        #plotx = np.arange(0,N+1)
        #ploty = np.zeros((0,N+1))
        plt.style.use('housestyle')
        fig = plt.figure()
       
        #plt.subplots_adjust(left=0.1,wspace=0.2,hspace=0.3)
        plt.suptitle(title.upper()+'-'+self.plot_Title)
        start=time.time()
        standardAxis = [0,0,0,0]#统一化的坐标
        for i in xrange(0,16):
      
            for res in result:
                x = np.dot(res[1:5],mask[i])
                y = res[0]
                if ploty.has_key(x):
                    ploty[x] +=y
                else:
                    ploty[x] = y                  
            ax = plt.subplot(4,4,i+1)
   
            #开始绘图了
            plt.sca(ax)
            plt.title(self.fn_will_be_used[i],fontsize=10)
            #plt.title("f0")
            #x轴的扩展
            #plt.xlim(0,2*N+1)
            #plt.ylim(0,2*max(list(ploty.values())))
            # plt.plot(list(ploty.keys()),list(ploty.values()),'b')
            plt.bar(list(ploty.keys()),list(ploty.values()))
            standardAxis[0] = standardAxis[0] if standardAxis[0] < min(list(ploty.keys())) else min(list(ploty.keys()))
            standardAxis[1] = standardAxis[1] if standardAxis[1] > max(list(ploty.keys())) else max(list(ploty.keys()))
            standardAxis[2] = standardAxis[2] if standardAxis[2] < min(list(ploty.values())) else min(list(ploty.values()))
            standardAxis[3] = standardAxis[3] if standardAxis[3] > max(list(ploty.values())) else max(list(ploty.values()))
            ploty.clear()    
        


        #统一下坐标
        for x in xrange(1,17):
            plt.subplot(4,4,x)
            plt.xlim(standardAxis[0]-1,standardAxis[1]+2)
            plt.ylim(standardAxis[2],standardAxis[3]+2)

        plt.savefig(self.plot_Path+'SL/'+self._getFileName(N,2,power,title,'G','P','null',operation))#保存文件了~走起
        plt.close('all')
        # plt.show()
        print time.time()-start    
    
    def _get_mask_by_type(self,mtype='sl'):
        """根据类型返回不同的mask"""
        if mtype=='sl':
            print "SL"
            return self.mask
        elif mtype=='f':
            tempMask = self.mask.copy()
            #采用交换方式得到新的Mask
            for x in [0,4,8,12]:
                m = tempMask[x+1].copy()
                tempMask[x+1] = tempMask[x+2] #矩阵中的第二列与第三列交换
                tempMask[x+2] = m
                self.fn_will_be_used[x+1] = self.fn_std[x+2]
                self.fn_will_be_used[x+2] = self.fn_std[x+1]

            return tempMask
        elif mtype=='c':
            print "C"
            tempMask = self.mask.copy()
            m = tempMask.copy()
            #采用赋值方式得到新的mask
            for x in [0,1]:
                for y in xrange(0,8):
                    m[x*8+(y%4)*2+y/4] = tempMask[x*8+y]
                    self.fn_will_be_used[x*8+(y%4)*2+y/4] = self.fn_std[x*8+y]
            return m

    
    def _plothist(self,N,mtype,power=1,opcode="1111"):
        self._plot_sl(N,self._get_mask_by_type(mtype),mtype,power,opcode)


if __name__ == '__main__':
    a = PlotHist()
    a._plothist(20,'sl')

# End of plotHist.py