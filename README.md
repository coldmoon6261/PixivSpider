## 关于此p站爬虫
目的是为了爬p站([pixiv](https://www.pixiv.net))每日排行榜里面插画类的图，一次性跑5天的。完成度还算将就，只不过还有以下较大的问题：

### 1.没有设置排行榜前几
设置排行榜前几的时候还要注意最好在section前实现，要不然有大量冗余
好像默认的50张也是可以的

### 2.图片格式问题
解决了格式问题，现在允许.jpg以及.png格式的图片保存

### 3.多张图片问题
在一个界面下多张图片还无法解决，只会下载第一张。后续会解决这个问题。

### 4.莫名奇妙的错误
在cmd里面按下Ctrl+C跳过

### 5.下载速度
下载速度没有注意，我一开始就是朝着原图去的，可能会比较慢，听说多线程好像快一点不知道是不是真的，可能以后会尝试（等我学会吧）

当然后面可能会显示当前图片的下载进度与速度，预想速度为0的时候按Ctrl+C比较好

### 6.更多高级功能
看这个代码就应该知道我还是个初学者，代码之后肯定是会优化的。
如果继续做可能会做一个GUI吧，到时候在界面改变设置什么的，比如说搜索某作者来下载TA的图片，又或者其它我暂时想不出来的功能。