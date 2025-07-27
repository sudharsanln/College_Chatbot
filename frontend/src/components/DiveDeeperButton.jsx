import React from 'react';

function DiveDeeperButton({onClick}) {
    return (
        <div className="dive-deeper-button-container">
            <button onClick={onClick} className="dive-deeper-button">
                Dive Deeper
            </button>
        </div>
    );
}

export default DiveDeeperButton;