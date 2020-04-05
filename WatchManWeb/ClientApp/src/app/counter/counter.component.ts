import { Component, ViewChild, ElementRef } from '@angular/core';
@Component({
  selector: 'app-counter-component',
  templateUrl: './counter.component.html',
  styleUrls: ['./counter.component.css']
})
export class CounterComponent {
  name = "Angular";
  @ViewChild("videoPlayer", { static: false }) videoplayer: ElementRef;
  isPlay: boolean = false;

  public toggleVideo(event: any) {
    this.videoplayer.nativeElement.play();
  }

 public analize() {
    let myVideo = document.getElementById("my_video_1");
    console.log("analize")
  }

  public makeScreen() {
    let myVideo = document.getElementById("my_video_1");
    console.log("screen capture")
  }
}
