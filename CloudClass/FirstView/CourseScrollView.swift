//
//  CourseScrollView.swift
//  CloudClass
//
//  Created by 张雨帆 on 2019/6/27.
//  Copyright © 2019 张雨帆. All rights reserved.
//

import UIKit

class CourseScrollView: UIScrollView {

    var courses = [
        ["name": "风暴之灵", "pic": "timg-1.jpg"],
        ["name": "末日使者", "pic": "timg.jpg"],
        ["name": "默认头像", "pic": "默认头像.jpg"],
    ]
    
    // Only override draw() if you perform custom drawing.
    // An empty implementation adversely affects performance during animation.
    override func draw(_ rect: CGRect) {
        //设置scrollView的内容总尺寸
        self.contentSize = CGSize(
            width: CGFloat(self.bounds.width) * CGFloat(self.courses.count),
            height: self.bounds.height
        )
        // 关闭滚动条显示
        self.showsHorizontalScrollIndicator = false
        self.showsVerticalScrollIndicator = false
        self.scrollsToTop = false
        // 滚动时只能停留到某一页
        self.isPagingEnabled = true
        //添加页面到滚动面板里
        let size = self.bounds.size
        for (seq,course) in courses.enumerated() {
            let page = UIView()
            let imageView=UIImageView(image:UIImage(named:course["pic"]!))
            page.addSubview(imageView);
            page.backgroundColor = UIColor.green
            let lbl = UILabel(frame: CGRect(x: 0, y: 20, width: 100, height: 20))
            lbl.text = course["name"]
            page.addSubview(lbl)
            
            page.frame = CGRect(x: CGFloat(seq) * size.width, y: 0,
                                width: size.width, height: size.height)
            self.addSubview(page)
        }
    }
}
