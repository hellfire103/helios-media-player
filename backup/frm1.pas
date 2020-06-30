unit frm1;

{$mode objfpc}{$H+}

interface

uses
  Classes, SysUtils, Forms, Controls, Graphics, Dialogs, ExtCtrls, Buttons,
  ComCtrls, StdCtrls, PasLibVlcPlayerUnit;

type

  { TForm1 }

  TForm1 = class(TForm)
    BitBtn1: TBitBtn;
    BitBtn2: TBitBtn;
    BitBtn3: TBitBtn;
    BitBtn4: TBitBtn;
    lblTime: TLabel;
    OpenDialog1: TOpenDialog;
    Panel1: TPanel;
    trkPosition: TTrackBar;
    trkVolume: TTrackBar;
    vlcPlayer: TPasLibVlcPlayer;
    procedure BitBtn1Click(Sender: TObject);
    procedure BitBtn2Click(Sender: TObject);
    procedure BitBtn3Click(Sender: TObject);
    procedure BitBtn4Click(Sender: TObject);
    procedure trkPositionMouseDown(Sender: TObject; Button: TMouseButton;
      Shift: TShiftState; X, Y: Integer);
    procedure trkPositionMouseUp(Sender: TObject; Button: TMouseButton;
      Shift: TShiftState; X, Y: Integer);
    procedure trkVolumeChange(Sender: TObject);
    procedure vlcPlayerMediaPlayerLengthChanged(Sender: TObject; time: Int64);
    procedure vlcPlayerMediaPlayerTimeChanged(Sender: TObject; time: Int64);
  private

  public

  end;

var
  Form1: TForm1;

implementation

{$R *.lfm}

{ TForm1 }

procedure TForm1.BitBtn1Click(Sender: TObject);
begin
  vlcPlayer.Resume();
end;

procedure TForm1.BitBtn2Click(Sender: TObject);
begin
  vlcPlayer.Pause();
end;

procedure TForm1.BitBtn3Click(Sender: TObject);
begin
  if OpenDialog1.Execute then begin
    vlcPlayer.Play(WideString(OpenDialog1.FileName));
    Caption := OpenDialog1.FileName;
  end;
end;

procedure TForm1.BitBtn4Click(Sender: TObject);
var
  url: string;
begin
  url := InputBox('Media URL', 'Please enter media URL/MRL', '');
  if url <> '' then begin
    vlcPlayer.Play(WideString(url));
    Caption := url;
  end;
end;

procedure TForm1.trkPositionMouseDown(Sender: TObject; Button: TMouseButton;
  Shift: TShiftState; X, Y: Integer);
begin
  trkPosition.Tag := 1;
end;

procedure TForm1.trkPositionMouseUp(Sender: TObject; Button: TMouseButton;
  Shift: TShiftState; X, Y: Integer);
begin
  vlcPlayer.SetVideoPosInMs(trkPosition.Position);
  trkPosition.Tag := 0;
end;

procedure TForm1.trkVolumeChange(Sender: TObject);
begin
  vlcPlayer.SetAudioVolume(trkVolume.Position);
end;

procedure TForm1.vlcPlayerMediaPlayerLengthChanged(Sender: TObject; time: Int64
  );
begin
  trkPosition.Max := vlcPlayer.GetVideoLenInMs();
end;

procedure TForm1.vlcPlayerMediaPlayerTimeChanged(Sender: TObject; time: Int64);
begin
  if trkPosition.Tag = 0 then // not dragging with mouse
     trkPosition.Position := vlcPlayer.GetVideoPosInMs();
  lblTime.Caption:=vlcPlayer.GetVideoPosStr('hh:mm:ss');
end;

end.

