//
//  PageControl.swift
//  CloudClass
//
//  Created by 张雨帆 on 2019/6/27.
//  Copyright © 2019 张雨帆. All rights reserved.
//

import UIKit

class PageControl: UIPageControl {

    // Only override draw() if you perform custom drawing.
    // An empty implementation adversely affects performance during animation.
    override func draw(_ rect: CGRect) {
//        self.backgroundColor = UIColor.clear
        self.numberOfPages = 3
        self.currentPage = 0
    }
 

}
