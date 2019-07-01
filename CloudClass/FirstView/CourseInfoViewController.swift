//
//  CourseInfoViewController.swift
//  CloudClass
//
//  Created by 张雨帆 on 2019/6/28.
//  Copyright © 2019 张雨帆. All rights reserved.
//  详细课程界面

import UIKit


class CourseInfoViewController: UIViewController {

    var demotitle = "ahhh"
    
    
    @IBOutlet var demoTitle: UILabel!
    override func viewDidLoad() {
        super.viewDidLoad()
        demoTitle.text = demotitle
        // Do any additional setup after loading the view.
    }
    

    /*
    // MARK: - Navigation

    // In a storyboard-based application, you will often want to do a little preparation before navigation
    override func prepare(for segue: UIStoryboardSegue, sender: Any?) {
        // Get the new view controller using segue.destination.
        // Pass the selected object to the new view controller.
    }
    */

}
