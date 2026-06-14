import argparse
import sys
from src.training.train_pipeline import run_training
from src.evaluation.evaluate import evaluate_model

def main():
    parser = argparse.ArgumentParser(description="AgriVision AI - Model Training Entrypoint")
    parser.add_argument("--dataset_path", type=str, default=None, help="Path to PlantVillage dataset folder")
    parser.add_argument("--epochs", type=int, default=None, help="Number of training epochs")
    parser.add_argument("--batch_size", type=int, default=None, help="Batch size for training")
    parser.add_argument("--quick_mode", type=str, default=None, help="Use subset of images per class for fast training (True/False)")
    parser.add_argument("--max_samples", type=int, default=None, help="Max samples per class in quick mode")
    
    args = parser.parse_args()
    
    # Parse quick_mode string to boolean if provided
    quick_mode = None
    if args.quick_mode is not None:
        quick_mode = args.quick_mode.lower() in ("true", "1", "yes")
        
    try:
        # 1. Run model training
        model, history, test_data, all_dirs, training_duration = run_training(
            dataset_path=args.dataset_path,
            epochs=args.epochs,
            batch_size=args.batch_size,
            quick_mode=quick_mode,
            max_samples=args.max_samples
        )
        
        # 2. Run model evaluation
        epochs_trained = args.epochs if args.epochs is not None else len(history.history['accuracy'])
        evaluate_model(
            model=model,
            history=history,
            test_data=test_data,
            all_dirs=all_dirs,
            training_duration=training_duration,
            epochs_trained=epochs_trained
        )
        
    except Exception as e:
        print(f"Error during training pipeline execution: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)

if __name__ == "__main__":
    main()
