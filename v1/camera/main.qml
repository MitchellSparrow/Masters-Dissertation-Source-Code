import QtQuick 2.0
import CvbQuick 1.0 as CvbQuick


Rectangle {
    id: page
    width: 320; height: 480
    color: "lightgray"
    

    CvbQuick.ImageView
    {
        id: view
        anchors.fill : parent
        image : mainImage
    }

    Text {
        id: helloText
        text: String(view.hoverPixel)
        y: 30
        anchors.horizontalCenter: page.horizontalCenter
        font.pointSize: 24; font.bold: true
    }
}
