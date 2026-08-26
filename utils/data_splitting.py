# Training(80%), Validation(10%), Testing(10%)
def split(dataset, train_ratio = 0.8, val_ratio = 0.1, test_ratio = 0.1):
    rows = len(dataset)

    train_rows = int(train_ratio * rows)
    val_rows = int(val_ratio * rows)
    test_rows = int(test_ratio * rows)

    training_dataset = dataset.iloc[:train_rows]
    validation_dataset = dataset.iloc[train_rows:train_rows + val_rows]
    testing_dataset = dataset.iloc[train_rows + val_rows:]

    return training_dataset, validation_dataset, testing_dataset
