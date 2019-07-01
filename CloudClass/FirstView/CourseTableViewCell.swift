//
//  CourseTableViewCell.swift
//  CloudClass
//
//  Created by 张雨帆 on 2019/6/27.
//  Copyright © 2019 张雨帆. All rights reserved.
//

import UIKit

class CourseTableViewCell: UITableViewCell {
    
    @IBOutlet var title: UILabel!
    
    @IBOutlet var subTitle: UILabel!
    
    override func awakeFromNib() {
        super.awakeFromNib()
        // Initialization code
    }

    override func setSelected(_ selected: Bool, animated: Bool) {
        super.setSelected(selected, animated: animated)

        // Configure the view for the selected state
    }
    
}
