//
//  FirstViewController.swift
//  CloudClass
//
//  Created by 张雨帆 on 2019/6/24.
//  Copyright © 2019 张雨帆. All rights reserved.
//

import UIKit

class FirstViewController: UIViewController, UIScrollViewDelegate, UITableViewDataSource, UITableViewDelegate {
    
    static var UserName = "" //用户名
    static var UserType = "" //用户类型
    
    @IBOutlet var ScrollView: UIScrollView!
    @IBOutlet var PageControl: UIPageControl!
    @IBOutlet var CourseTable: UITableView!
    
    // 上方分页视图被点击时调用
    @IBAction func pageChanged(_ sender: UIPageControl) {
        //根据点击的页数，计算scrollView需要显示的偏移量
        var frame = ScrollView.frame
        frame.origin.x = frame.size.width * CGFloat(sender.currentPage)
        frame.origin.y = 0
        //展现当前页面内容
        ScrollView.scrollRectToVisible(frame, animated:true)
    }
    
    // 页面出现前调用
    override func viewWillAppear(_ animated: Bool) {
        super.viewWillAppear(animated)
        CourseTable.reloadData()
    }
    
    // 页面设置好后调用
    override func viewDidLoad() {
        super.viewDidLoad()
        // 协议代理，在本类中处理滚动事件
        ScrollView.delegate = self
        
        // 注册xib文件作为表视图的一行
        let xib = UINib(nibName: "CourseTableViewCell", bundle: nil)
        CourseTable.register(xib, forCellReuseIdentifier: "CourseTableViewCell")
        // 设置CourseTable数据源和代理方法
        CourseTable.dataSource = self
        CourseTable.delegate = self
        CourseTable.rowHeight = 82.5
        
    }
    
    override func didReceiveMemoryWarning() {
        super.didReceiveMemoryWarning()
        // Dispose of any resources that can be recreated.
    }
    
    //UIScrollViewDelegate方法，每次滚动结束后调用
    func scrollViewDidEndDecelerating(_ scrollView: UIScrollView) {
        //通过scrollView内容的偏移计算当前显示的是第几页
        let page = Int(ScrollView.contentOffset.x / ScrollView.frame.size.width)
        //设置pageController的当前页
        PageControl.currentPage = page
    }
    
    // 设置表中分几节
    func numberOfSections(in tableView: UITableView) -> Int {
        return 3
    }
    
    // 设置表中行数
    func tableView(_ tableView: UITableView, numberOfRowsInSection section: Int) -> Int {
        return 4
    }
    
    // 设计某一行
    func tableView(_ tableView: UITableView, cellForRowAt indexPath: IndexPath) -> UITableViewCell {
        let cell = tableView.dequeueReusableCell(withIdentifier: "CourseTableViewCell", for: indexPath) as! CourseTableViewCell
        cell.title.text = "课程名"
        cell.subTitle.text = "类别、星级"
        return cell
    }
    
    // 点击某一行跳转
    func tableView(_ tableView: UITableView, didSelectRowAt indexPath: IndexPath) {
//        let threeVC = CourseInfoViewController()
//        self.navigationController?.pushViewController(threeVC, animated: true)
        performSegue(withIdentifier: "showInfo", sender: tableView.cellForRow(at: indexPath))
    }
    
    override func prepare(for segue: UIStoryboardSegue, sender: Any?) {
        let indexPath = CourseTable.indexPath(for: sender as! UITableViewCell)!
        let listVC = segue.destination as! CourseInfoViewController //对新视图控制器的引用
        listVC.demotitle = "大家好，我是第\(indexPath.section + 1)类的第\(indexPath.row + 1)节课"
    }

}

