import PropTypes from "prop-types";

const ESC_KEY_CODE = 27;

const SearchInput = ({ placeholderText, onInputChange, searchValue }) => {

  const onKeyDown = (event) => {
    if (event.keyCode === ESC_KEY_CODE) {
      onInputChange({ target: { value: '' } });
    }
  }

  return (
    <input
      type="text"
      placeholder={placeholderText}
      onChange={onInputChange}
      onKeyDown={onKeyDown}
      value={searchValue}
    />
  );
};

SearchInput.propTypes = {
    placeholderText: PropTypes.string,
    onInputChange: PropTypes.func,
    searchValue: PropTypes.string,
}

export default SearchInput;