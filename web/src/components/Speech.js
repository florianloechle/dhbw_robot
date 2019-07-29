/** @format */

import React from 'react';
import SpeechRecognition from 'react-speech-recognition';
import clsx from 'clsx';

class Speech extends React.Component {
  state = {
    result: null,
  };
  componentDidUpdate(prevProps) {
    if (
      prevProps.transcript !== this.props.transcript &&
      this.props.transcript !== ''
    ) {
      this.checkForMatches();
    }
  }
  checkForMatches() {
    const { transcript, targets, resetTranscript } = this.props;
    const spoken = transcript.toLowerCase();
    if (Array.isArray(targets)) {
      for (let target of targets) {
        if (spoken.indexOf(target.toLowerCase()) !== -1) {
          resetTranscript();
          return this.setState({ result: target }, () => {
            this.props.onRecognized(this.state.result);
          });
        }
      }
    } else {
      if (spoken.indexOf(targets.toLowerCase()) !== -1) {
        resetTranscript();
        return this.setState({ result: targets });
      }
    }
  }
  handleSpeech = event => {
    const { startListening, listening, resetTranscript } = this.props;
    if (!listening) {
      startListening();
    } else {
      resetTranscript();
    }
  };
  render() {
    const { browserSupportsSpeechRecognition, listening } = this.props;
    if (!browserSupportsSpeechRecognition) {
      return (
        <div className="speech disabled">
          <h4>Dein Browser unterstützt keine Spracheingabe!</h4>
          <span role="img" aria-label="crying emoji">
            😭
          </span>
        </div>
      );
    }
    return (
      <div className="speech-container">
        <button className="speech" onClick={this.handleSpeech}>
          <div className={clsx('mic', listening && 'active')}>
            <div className="mic_body">
              <div className="mic_pill" />
              <div className="mic_hole" />
              <div className="mic_stand" />
              <div className="mic_bottom" />
            </div>
            <div className="dots">
              <div className="dots_left" />
              <div className="dots_middle" />
              <div className="dots_right" />
            </div>
          </div>
        </button>
      </div>
    );
  }
}

export default SpeechRecognition({ autoStart: false, continuous: false })(
  Speech
);
