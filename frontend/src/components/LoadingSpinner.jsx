import classes from './LoadingSpinner.module.css'

export default function LoadingSpinner() {
    return (
        <div className="loading-container">
            <div className={classes.loadingSpinner}>
                <span className="loading-spinner-text"/>
            </div>
        </div>
    );
}